# AWS Databricks Lakehouse Project

## Overview

This project demonstrates an end-to-end Lakehouse Data Engineering solution using AWS S3, Databricks, PySpark, and Delta Lake.

The solution follows the Medallion Architecture (Bronze, Silver, Gold) pattern and implements incremental batch processing, data quality validation, Delta MERGE operations, and business-focused aggregations.

---

## Project Architecture

```text
Transaction Batch Files
         │
         ▼
    AWS S3 Raw Layer
         │
         ▼
    Bronze Delta Layer
         │
         ▼
    Silver Delta Layer
         │
         ▼
     Gold Delta Layer
         │
         ▼
Business Reporting & Analytics
```

---

## Technologies Used

- AWS S3
- AWS IAM
- Databricks
- PySpark
- Delta Lake

---

## Dataset Information

Dataset: Ecommerce Transactions Dataset

Total Records: 50,000

Key Columns:

- Transaction_ID
- User_Name
- Age
- Country
- Product_Category
- Purchase_Amount
- Payment_Method
- Transaction_Date

---

## Medallion Architecture

### Raw Layer

Purpose:

- Landing zone for incoming source files
- Stores original files without modifications
- Enables replayability and auditability

Storage Location:

```text
s3://ecommerce-projectbucket/raw/incoming/
```

---

### Bronze Layer

Purpose:

- Ingest raw transaction data
- Standardize source records
- Store data in Delta format

Key Transformations:

- Convert Transaction_Date to DateType
- Add ingestion_timestamp
- Partition by Transaction_Date

Storage Location:

```text
s3://ecommerce-projectbucket/bronze/transactions/
```

---

### Silver Layer

Purpose:

- Create trusted business-ready transaction data
- Apply quality checks and cleansing

Data Quality Rules:

- Remove null Transaction_ID values
- Remove invalid Purchase_Amount values
- Remove duplicate Transaction_ID values

Derived Columns:

- transaction_year
- transaction_month
- transaction_day

Storage Location:

```text
s3://ecommerce-projectbucket/silver/transactions/
```

---

### Gold Layer

Purpose:

Provide analytics-ready datasets for business reporting.

Gold Tables:

#### Daily Sales

Metrics:

- Total Revenue
- Transaction Count

#### Country Sales

Metrics:

- Revenue by Country
- Transaction Count

#### Category Sales

Metrics:

- Revenue by Product Category
- Transaction Count

Storage Location:

```text
s3://ecommerce-projectbucket/gold/
```

---

## Incremental Processing

The project supports incremental batch processing.

Process Flow:

```text
New Batch File
        │
        ▼
Append To Bronze
        │
        ▼
Apply Silver Transformations
        │
        ▼
Delta MERGE Into Silver
        │
        ▼
Refresh Gold Aggregations
```

### Delta MERGE Logic

If Transaction_ID already exists:

- Update existing record

If Transaction_ID does not exist:

- Insert new record

Benefits:

- Incremental processing
- Reduced reload effort
- Prevention of duplicate records
- Support for future data corrections

---

## Delta Lake Features

This project uses Delta Lake to provide:

- ACID Transactions
- Schema Enforcement
- Reliable Data Processing
- Delta MERGE Support
- Transaction Logging
- Scalable Data Management

---

## Project Structure

```text
aws-databricks-lakehouse-project/

├── notebooks/
│   ├── 01_raw_to_bronze.py
│   ├── 02_bronze_to_silver.py
│   ├── 03_silver_to_gold.py
│   └── 04_incremental_batch_processing.py
│
├── docs/
│   └── AWS_Databricks_Lakehouse_Project.docx
│
├── screenshots/
│
└── README.md
```

---

## Key Features Implemented

- AWS S3 Data Lake
- Medallion Architecture
- PySpark Data Processing
- Delta Lake Storage
- Partitioning Strategy
- Data Quality Validation
- Incremental Batch Processing
- Delta MERGE Operations
- Business Aggregations

---

## Business Value

This solution enables:

- Daily Revenue Analysis
- Country-Wise Sales Analytics
- Product Category Performance Analysis
- Scalable Data Processing
- Trusted Reporting Datasets

---

## Learning Outcomes

Through this project, the following concepts were implemented and validated:

- AWS S3 Data Lake Design
- Databricks and AWS Integration
- PySpark Transformations
- Delta Lake Fundamentals
- Medallion Architecture
- Incremental ETL Processing
- Delta MERGE (UPSERT) Operations
- Data Quality Frameworks
- Analytics Data Modeling

---

## Future Enhancements

- Automated file discovery
- Databricks Workflows orchestration
- AWS Glue Data Catalog integration
- Event-driven processing using S3 notifications
- Monitoring and alerting
- Data quality dashboard

---

## Author

Syed Jaffar Hussain

AWS | Databricks | PySpark | Data Engineering

