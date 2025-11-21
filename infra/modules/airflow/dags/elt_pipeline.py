from airflow import DAG
from datetime import datetime
from src.extract_load import ExtractLoad
from src.load_to_postgres import LoadToPostgres
from airflow.operators.python import PythonOperator


def hello_world(**kwargs):
    print("Hello World!")
    return "Hello World geprint"

def run_extract_load(**kwargs):
    el = ExtractLoad(read_from_cache=True)
    el.el()

def run_load_to_postgres():
    lp = LoadToPostgres(read_from_cache=True)
    lp.execute()

# ----------------------------
# Define DAG
# ----------------------------
with DAG(
    dag_id="elt_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule=None,  # Manual trigger
    catchup=False
    ) as dag:
    
    # Task 1: Hello World 
    hello_world = PythonOperator(
        task_id="hello_world",
        python_callable=hello_world
    )

    # Task 2: Extract and load 
    extract_load_task = PythonOperator(
        task_id="extract_load",
        python_callable=run_extract_load
    )

    # Task 3: Load to Postgres
    load_to_postgres_task = PythonOperator(
        task_id="load_to_postgres",
        python_callable=run_load_to_postgres
    )

    # ----------------------------
    # Set task dependencies
    # ----------------------------
    hello_world >> extract_load_task >> load_to_postgres_task