<!--
   README.md  ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
   Project : SKU110K ETL Pipeline (Airflow + Docker)
   Author  : Hussein Elgamal · Data Engineer
   License : MIT
-->

# 🧠 SKU110K ETL Pipeline (Airflow + Docker)

> **End-to-end data-engineering pipeline** for downloading, preprocessing, validating, cataloging, and packaging the **[SKU110K](https://github.com/eg4000/SKU110K_CVPR19)** dataset – orchestrated with **Apache Airflow** and containerized with **Docker**.

This project automates the processing of the SKU110K dataset (~15 GB), which contains retail shelf images and annotations for object detection tasks. The pipeline handles ingestion, image resizing, data validation, conversion to COCO format, metadata generation, cloud uploads, and planogram data integration. It supports both Airflow-orchestrated workflows and standalone execution (e.g., in Google Colab).

| Stage | Description |
|-------|-------------|
| 📥 **Ingestion** | Downloads and extracts the raw SKU110K dataset (~15 GB). |
| 🧹 **Pre-process** | Resizes images to 1024×1024, normalizes pixel values, and scales annotation coordinates. |
| 🧪 **Validation** | Detects corrupted images and validates JSON/CSV annotations. |
| 🗃️ **Catalog** | Generates `catalog.json` with metadata and data lineage. |
| 📦 **Package** | Creates ZIP files for train, validation, and test splits. |
| ☁️ **Delivery** | Uploads processed data to MEGA cloud storage using **rclone**. |
| 🗺️ **Planogram** | Ingests shelf-layout data (JSON/CSV) and links to products. |

---

## 🚀 Tech Stack

| Tool | Role |
|------|------|
| **Python 3.11** | Core ETL logic and scripting. |
| **Apache Airflow 2.9** | Workflow orchestration and scheduling. |
| **Docker & docker-compose** | Containerized, reproducible environment. |
| **OpenCV / Pillow / NumPy** | Image processing and annotation handling. |
| **pandas / tqdm** | Data manipulation and progress tracking. |
| **rclone + MEGA** | Cloud storage integration for data delivery. |
| **PostgreSQL** | Metadata storage for Airflow. |
| **SQLite** | Storage for planogram data. |

---

## 📋 Prerequisites

Before setting up the project, ensure you have:
- **Docker** and **docker-compose** installed ([Docker Installation Guide](https://docs.docker.com/get-docker/)).
- **Git** for cloning the repository.
- A **MEGA** account with `rclone` configured ([rclone MEGA setup](https://rclone.org/mega/)).
- At least **20 GB** of disk space for the dataset and outputs.
- For Colab usage: A Google Drive account with the SKU110K dataset (`SKU110K_fixed.tar.gz`).
- Basic familiarity with Airflow, Python, and Docker.

---

## 📂 Repository Structure

```text
.
├── dags/                       # Airflow DAG definitions
│   └── sku110k_etl_dag.py     # Main ETL pipeline DAG
├── docker/
│   ├── Dockerfile             # Custom image for ETL tasks
│   └── requirements.txt       # Python dependencies
├── src/
│   ├── etl_pipeline.py        # Standalone ETL script (CLI)
│   └── sku110k_notebook.ipynb # Jupyter Notebook for Colab/local
├── data-catalog/
│   └── sample_catalog.json    # Example metadata output
├── sku110k_output/            # (Optional) Demo ZIP outputs
├── screenshots/               # Screenshots for README (optional)
├── .env.example               # Template for environment variables
├── docker-compose.yml         # Airflow + Postgres stack
├── screenshoots
├── LICENSE                    # MIT License
└── README.md                  # This file
