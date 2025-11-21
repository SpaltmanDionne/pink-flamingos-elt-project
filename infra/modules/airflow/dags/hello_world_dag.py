from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Functie die wordt uitgevoerd
def print_hello():
    print("Hello World!")
    return "Hello World geprint"

def print_goodbye():
    print("Tot ziens!")
    return "Goodbye geprint"

# Default argumenten voor de DAG
default_args = {
    'owner': 'jouw_naam',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Maak de DAG aan
dag = DAG(
    'hello_world_dag',
    default_args=default_args,
    description='Een simpele Hello World DAG',
    schedule=None, # Manual trigger 
    catchup=False # Voert geen oude runs uit
)

# Maak de tasks aan
task_hello = PythonOperator(
    task_id='print_hello',
    python_callable=print_hello,
    dag=dag,
)

task_goodbye = PythonOperator(
    task_id='print_goodbye',
    python_callable=print_goodbye,
    dag=dag,
)

# Definieer de volgorde: eerst hello, dan goodbye
task_hello >> task_goodbye