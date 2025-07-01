from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import psycopg2

def ingest_metadata():
    """
    Walks through the SKU110K dataset directory recursively and calculates total size in MB.
    """
    base_dir = "/opt/airflow/SKU110K"
    size_mb = 0
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            size_mb += os.path.getsize(file_path) / (1024 * 1024)

    metadata = {
        "dataset_name": "SKU110K",
        "version": "1.0",
        "size_mb": round(size_mb, 2),
        "created_date": datetime.now()
    }
    return metadata

def store_metadata(ti):
    """
    Connects to PostgreSQL and stores the dataset metadata into the data_catalog table.
    Creates the table if it doesn't exist.
    """
    metadata = ti.xcom_pull(task_ids='ingest_metadata')
    conn = psycopg2.connect(
        dbname="airflow",
        user="airflow",
        password="airflow",
        host="postgres"
    )
    cur = conn.cursor()

    # Create table if not exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS data_catalog (
            id SERIAL PRIMARY KEY,
            dataset_name VARCHAR(255),
            version VARCHAR(50),
            size_mb FLOAT,
            created_date TIMESTAMP
        );
    """)

    # Insert metadata
    cur.execute("""
        INSERT INTO data_catalog (dataset_name, version, size_mb, created_date)
        VALUES (%s, %s, %s, %s);
    """, (
        metadata['dataset_name'],
        metadata['version'],
        metadata['size_mb'],
        metadata['created_date']
    ))

    conn.commit()
    conn.close()

# Define the DAG
with DAG(
    dag_id="catalog_dag",
    start_date=datetime(2025, 6, 29),
    schedule_interval='@daily',
    catchup=False,
    description="Catalog DAG to track dataset metadata in PostgreSQL"
) as dag:

    task_ingest = PythonOperator(
        task_id="ingest_metadata",
        python_callable=ingest_metadata
    )

    task_store = PythonOperator(
        task_id="store_metadata",
        python_callable=store_metadata
    )

    task_ingest >> task_store
