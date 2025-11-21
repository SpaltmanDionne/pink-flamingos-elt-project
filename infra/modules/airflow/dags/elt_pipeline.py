from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
from airflow.operators.bash import BashOperator

from datetime import datetime

import os
import json
import requests
from io import BytesIO
from minio import Minio
from datetime import datetime
from src.extract_load import ExtractLoad


def hello_world(**kwargs):
    print("Hello World!")
    return "Hello World geprint"

def run_extract_load(**kwargs):
    el = ExtractLoad(read_from_cache=True)
    el.el()

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

    # Task 3: Transform with dbt 
    transform = BashOperator(
    task_id="transform_dbt",
    bash_command=(
        "dbt run "
        "--project-dir /opt/airflow/dbt_pink_flamingos "
        "--profiles-dir /opt/airflow"
        )
    )

    # ----------------------------
    # Set task dependencies
    # ----------------------------
    # hello_world >> extract_load_task 
    hello_world >> extract_load_task >> transform