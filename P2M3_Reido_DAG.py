# Identitas
'''
Nama : Reido
Batch : 040
'''

# Import Libraries
import pandas as pd
import numpy as np
import re
import datetime as dt
from airflow import DAG
from datetime import datetime, timedelta, time
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from elasticsearch import Elasticsearch, helpers

# Default Argument
default_args = {
    'owner': 'Reido',
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1)
}

# Fetch From Postgresql
def extract_data(**context):
    # Create Connection
    source_hook = PostgresHook(postgres_conn_id='postgres_airflow')
    source_conn = source_hook.get_conn()
    # Read Data
    raw_df = pd.read_sql('SELECT * FROM table_m3', source_conn)
    # Save Data Temporary
    temp_path = '/tmp/data_kotor.csv'
    raw_df.to_csv(temp_path, index=False)
    # Push to Xcom
    context['ti'].xcom_push(key='path_raw_data', value=temp_path)

# Data Cleaning
def transform_data(**context):
    def normalize_column(col_name):
        # Remove symbols like |, #, etc. -> replace with empty string
        col_name = re.sub(r'[^\w\s]', '', col_name)
        # Remove leading/trailing spaces
        col_name = col_name.strip()
        # Replace internal spaces with underscore
        col_name = re.sub(r'\s+', '_', col_name)
        # Convert to lowercase
        return col_name.lower()

    def clean_and_normalize_data(raw_df):
        # 1. Remove duplicates
        raw_df = raw_df.drop_duplicates()
        # 2. Normalize column names
        raw_df.columns = [normalize_column(col) for col in raw_df.columns]
        # 3. Convert the 'Date' column to datetime
        raw_df['date'] = pd.to_datetime(raw_df['date'], errors='coerce')
        # 4. Remove whitespace in object columns
        for col in raw_df.select_dtypes(include='object'):
            raw_df[col] = raw_df[col].str.strip()
        # 5. Remove rows with NaN values
        raw_df = raw_df.dropna()
        return raw_df

    # Pull from XCom
    ti = context['ti']
    raw_data_path = ti.xcom_pull(task_ids='extract_data', key='path_raw_data')

    # Load data
    raw_df = pd.read_csv(raw_data_path)

    # Clean it 
    clean_df = clean_and_normalize_data(raw_df)

    # Save cleaned data
    clean_path = '/tmp/P2M3_Reido_data_clean.csv'
    clean_df.to_csv(clean_path, index=False)

    # Push to XCom
    context['ti'].xcom_push(key='path_clean_data', value=clean_path)

# Post to Elasticsearch
def load_data(**context):
    # Pull from XCom
    ti = context['ti']
    clean_data_path = ti.xcom_pull(task_ids='transform_data', key='path_clean_data')
    # Read Data
    clean_df = pd.read_csv(clean_data_path)
    # Connect to Elasticsearch
    es = Elasticsearch('http://elasticsearch:9200')
    # Index name
    index_name = 'car_sales_cleaned'
    # List of actions
    actions = [
        {
            "_index": index_name,
            "_id": row['car_id'],
            "_source": row.to_dict()
        }
        for _, row in clean_df.iterrows()
    ]

    # Sent bulk
    helpers.bulk(es, actions)


with DAG (
    'pipeline_Reido',
    description = 'Pipeline Car Sales',
    default_args = default_args,
    start_date = datetime(2024, 11, 1, 9, 10)  - timedelta(hours=7),
    schedule_interval = '10-30/10 9 * * 6',
    catchup = True,
    max_active_runs=10
) as dag :
    
    # Task 1
    extract = PythonOperator(
        task_id = 'extract_data',
        python_callable = extract_data,
        provide_context = True
    )

    # Task 2
    transform = PythonOperator(
        task_id = 'transform_data',
        python_callable = transform_data,
        provide_context = True
    )
    
    # Task 3
    load = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        provide_context=True
    )

    # flow task
    extract >> transform >> load