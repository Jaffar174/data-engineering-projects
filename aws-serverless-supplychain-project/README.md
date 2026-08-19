# AWS Serverless Event-Driven Supply Chain Data Pipeline

## Overview

Built an end-to-end serverless data engineering pipeline using AWS services to automatically process newly arrived supply chain data files.

## Technologies Used

- Amazon S3
- AWS Lambda
- AWS Glue
- AWS Glue Crawlers
- AWS Glue Catalog
- Amazon Athena
- AWS IAM
- Amazon CloudWatch
- Python

## Architecture

```text
Supply Chain CSV Files
        ↓
Amazon S3
        ↓
S3 Event Notification
        ↓
AWS Lambda
        ↓
AWS Glue ETL Job
        ↓
Glue Job Bookmark
        ↓
Parquet Files
        ↓
Glue Catalog
        ↓
Amazon Athena
```

## Key Features

- Event-Driven Architecture
- Lambda Triggered ETL Processing
- Incremental Processing using Glue Job Bookmarks
- CSV to Parquet Conversion
- Athena Analytics
- Serverless Data Engineering

## Project Files

- Detailed project documentation available in the docs folder.
- Lambda source code available in the lambda folder.

## Author

Syed Jaffar Hussain

AWS | AWS Glue | Athena | Lambda | Data Engineering
