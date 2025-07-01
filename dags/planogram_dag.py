from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import psycopg2
from datetime import datetime

def ingest_planogram():
    df = pd.read_csv('/opt/airflow/data/sku_data.csv')
    return df.to_dict('records')

def link_to_sku(ti):
    planogram = ti.xcom_pull(task_ids='ingest_planogram')
    return [
        {
            'product_id': p['sku'],
            'shelf_location': f"Shelf_{p['sku'][-1]}",
            'discounted_price': p['discounted_price']
        }
        for p in planogram
    ]

def store_planogram(ti):
    planogram = ti.xcom_pull(task_ids='link_to_sku')
    conn = psycopg2.connect(dbname="airflow", user="airflow", password="airflow", host="postgres")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS planogram (
            id SERIAL PRIMARY KEY,
            product_id VARCHAR(50),
            shelf_location VARCHAR(100),
            discounted_price FLOAT
        )
    """)
    for record in planogram:
        cur.execute(
            "INSERT INTO planogram (product_id, shelf_location, discounted_price) VALUES (%s, %s, %s)",
            (record['product_id'], record['shelf_location'], record['discounted_price'])
        )
    conn.commit()
    conn.close()

with DAG('planogram_dag', start_date=datetime(2025, 6, 29), schedule_interval='@daily', catchup=False) as dag:
    t1 = PythonOperator(task_id='ingest_planogram', python_callable=ingest_planogram)
    t2 = PythonOperator(task_id='link_to_sku', python_callable=link_to_sku)
    t3 = PythonOperator(task_id='store_planogram', python_callable=store_planogram)
    t1 >> t2 >> t3
