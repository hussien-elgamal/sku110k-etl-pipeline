from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd

def extract_transform_load():
    # Extract: Read from the input CSV file
    input_file = '/opt/airflow/data/input_sku_data.csv'
    df = pd.read_csv(input_file)
    
    # Transform: Add a discount column (10% discount)
    df['discounted_price'] = df['price'] * 0.9
    
    # Load: Save to the output CSV file
    output_file = '/opt/airflow/data/sku_data.csv'
    df.to_csv(output_file, index=False)
    print(f"ETL process completed! Saved to {output_file}")

with DAG('sku110k_etl', start_date=datetime(2025, 6, 22), schedule_interval='@daily') as dag:
    task = PythonOperator(
        task_id='etl_task',
        python_callable=extract_transform_load
    )