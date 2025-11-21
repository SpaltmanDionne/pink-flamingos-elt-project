from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# ----------------------------
# Python functions for tasks
# ----------------------------

def extract(**kwargs):
    print("Running extract step")
    return {"data": [1, 2, 3]}

def load(**kwargs):
    # Haal de task_instance op uit de keyword arguments 
    # task_instance (ti) bevat informatie over de huidige task run
    ti = kwargs["ti"]
    data = ti.xcom_pull(task_ids="extract")
    print(f"Loading data: {data}")


# ----------------------------
# Define DAG
# ----------------------------
with DAG(
    dag_id="elt_skeleton_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,  # Manual trigger
    catchup=False
) as dag:

    # Task 1: Extract
    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract
    )

    # Task 2: Load
    load_task = PythonOperator(
        task_id="load",
        python_callable=load
    )

    # ----------------------------
    # Set task dependencies
    # ----------------------------
    extract_task >> load_task