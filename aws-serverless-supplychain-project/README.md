# AWS Serverless Event-Driven Supply Chain Data Pipeline

## Overview

This project demonstrates an end-to-end serverless data engineering pipeline built using AWS services. The solution automatically processes newly arrived supply chain data files using an event-driven architecture and makes curated datasets available for analytics through Amazon Athena.

The pipeline leverages Amazon S3, AWS Lambda, AWS Glue, Glue Catalog, Athena, and Glue Job Bookmarks to support automated incremental processing while preventing duplicate ingestion.

---

## Project Architecture

```text
Supply Chain CSV Files
          │
          ▼
      Amazon S3
      Raw Layer
          │
          ▼
 S3 Event Notification
          │
          ▼
      AWS Lambda
          │
          ▼
     AWS Glue ETL
          │
          ▼
  Glue Job Bookmark
          │
          ▼
 Parquet Processed Data
          │
          ▼
    AWS Glue Catalog
          │
          ▼
      Amazon Athena
```

---

## Technologies Used

- Amazon S3
- AWS Lambda
- AWS Glue ETL
- AWS Glue Crawlers
- AWS Glue Catalog
- Amazon Athena
- AWS IAM
- Amazon CloudWatch
- Python

---

## Dataset Information

### Dataset

Supply Chain Analytics Dataset

### Domain

Supply Chain and Logistics

### Dataset Preparation

- Removed unnecessary columns to simplify processing.
- Added a synthetic shipment_date column for time-based analytics.
- Split the dataset into multiple files to simulate periodic file arrivals.

### Files Used

```text
supply_chain_batch_01.csv
supply_chain_batch_02.csv
supply_chain_batch_03.csv
supply_chain_batch_04.csv
supply_chain_batch_05.csv
```

Each batch contains 20 records.

---

## Raw Layer

### Purpose

- Store source files without modification.
- Serve as the landing zone for incoming data.
- Trigger downstream processing.

### Storage Location

```text
s3://supplychainbuckett/raw/incoming/
```

---

## AWS Glue Catalog

### Database

```text
supply_chain_db
```

### Raw Table

```text
incoming
```

### Benefits

- Automatic schema discovery
- Centralized metadata management
- Integration with Athena and Glue ETL

---

## AWS Glue ETL Processing

### Glue Job

```text
supplychainetljob
```

### Processing Logic

- Read incoming CSV files from Amazon S3.
- Convert CSV data into Parquet format.
- Store processed data in the curated layer.
- Support incremental processing using Glue Job Bookmarks.

### Output Format

```text
Parquet
```

### Processed Location

```text
s3://supplychainbuckett/processed/supplychain/
```

---

## Incremental Processing

### Problem

Without incremental processing, AWS Glue reprocesses all files during every execution, resulting in duplicate records.

### Solution

AWS Glue Job Bookmarks were enabled.

### Validation

```text
Batch 1 Uploaded
        ↓
20 Records

Batch 2 Uploaded
        ↓
40 Records
```

Only newly arrived files are processed.

### Benefits

- Prevents duplicate processing
- Improves efficiency
- Reduces compute cost
- Supports scalable file ingestion

---

## Event-Driven Architecture

### Lambda Function

```text
trigger-glue-job
```

### Workflow

```text
New File Uploaded
         ↓
S3 Event Notification
         ↓
AWS Lambda
         ↓
AWS Glue ETL Job
```

### Outcome

AWS Glue processing is automatically triggered whenever a new file arrives in the raw S3 location.

---

## Processed Layer

### Processed Table

```text
supplychain
```

### Format

```text
Parquet
```

### Benefits

- Faster query performance
- Reduced storage size
- Lower Athena query cost
- Analytics-ready datasets

---

## Athena Analytics

Processed Parquet datasets are queried through Amazon Athena.

### Sample Queries

#### Record Count

```sql
SELECT COUNT(*)
FROM supplychain;
```

#### Reve*ue by Location

```sql
SELECT
    *ocation,
    SUM*revenue_generated) AS total_revenu*
FROM*supplychain
GROUP BY location;
```*
#### Average Shipping Cost by Car*ier

```sql
SELECT
    shipping_ca*riers,
    AVG(shipping_costs) AS *vg_shipping_cost
FROM supplychain
*ROUP BY shipping_carriers;
``*

#### Supplier Defect Analysis

`*`sql
SELECT
    supplier_name,
   *AVG(defect*rates) AS avg_defect_rate
FROM sup*lychain
GROUP BY supplier_name;
``*

---

## Monitoring

### Amazon C*oudWatch

CloudWatch*is used for:

- Lambda execution m*nitoring
- Glue job monitoring
- E*ror troubleshooting
- Event*trigger validation

---

## Key Fe*tures Implemented

-*Amazon S3 Data Lake
- Event-*riven Architecture
- AWS Lambda In*egration
- AWS Glue ETL Jobs
- AWS*Glue Crawlers*- AWS Glue Catalog
- Amazon Athena*Analytics
- CSV to Parquet Convers*on
- Increment*l Processing
- Glue Job Bookmarks
* Serverless Data Engineering

---
*## Business Value

*his solution enables:

- Automated*file ingestion
- Event-driven ETL *rocessing
- Incremental data proce*sing
- Supply chain analytics
- Se*verless*reporting*architecture
- Optimized analytica* querying

---

## Learning Outcom*s

Through this project, the follo*ing concepts were implemented and *alidated:

- AWS S3 Data Lake Desi*n
- AWS Lambda Automation
- AWS Gl*e ETL Development
- AWS Glue Catal*g Management
- AWS Glue Crawlers
-*Athena Analytics
- Event-Driven Pr*cessing
- Incremental Processing u*ing Glue Job Bookmarks
- Parquet O*timization
- Serverless Data Engin*ering Architecture

---

## Future*Enhancements

- Add data quality v*lidation framework
- Partition pro*essed datasets by date
- Archive s*ccessfully processed files
- Imple*ent operational dashboards
- Add a*erting and notification mechanisms*
---

## Project Structure

```tex*
aws-serverless-supplychain-projec*/

├── docs/
│   └── AWS_Serverles*_Event_Driven_SupplyChain_Data_Pip*line.docx
│
├── lambda/
│   └── la*bda_function.py
│
└── README.md
``*

---

## Author

Syed Jaff*r Hussain

AWS | AWS Glue | Athena*| Lambda | Data Engineering
