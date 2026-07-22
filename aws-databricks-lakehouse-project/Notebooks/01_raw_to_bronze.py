# Databricks notebook source
# MAGIC %md
# MAGIC Purpose:
# MAGIC Ingest raw transaction files from S3 into the Bronze layer.
# MAGIC
# MAGIC Source:
# MAGIC s3://ecommerce-projectbucket/raw/incoming/
# MAGIC
# MAGIC Target:
# MAGIC s3://ecommerce-projectbucket/bronze/transactions/
# MAGIC
# MAGIC Key Transformations:
# MAGIC - Convert Transaction_Date to DateType
# MAGIC - Add ingestion_timestamp
# MAGIC - Partition by Transaction_Date
# MAGIC - Store as Delta format

# COMMAND ----------

display(
dbutils.fs.ls("s3://ecommerce-projectbucket/")
)

# COMMAND ----------

display(
dbutils.fs.ls(

"s3://ecommerce-projectbucket/raw/incoming/"
)
)

# COMMAND ----------

df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(
        "s3://ecommerce-projectbucket/raw/incoming/batch_1.csv"
    )
)

display(df)

# COMMAND ----------

df.count()

# COMMAND ----------

from pyspark.sql.functions import (
    current_timestamp,
    to_date,
    col
)

bronze_df = (
    df
    .withColumn(
        "Transaction_Date",
        to_date(col("Transaction_Date"))
    )
    .withColumn(
        "ingestion_timestamp",
        current_timestamp()
    )
)

# COMMAND ----------

bronze_df.display()

# COMMAND ----------

bronze_df.printSchema()

# COMMAND ----------

bronze_df.write \
    .format("delta") \
    .mode("overwrite") \
    .partitionBy("Transaction_Date") \
    .save(
        "s3://ecommerce-projectbucket/bronze/transactions/"
    )

# COMMAND ----------

bronze_delta = spark.read.format("delta").load(
    "s3://ecommerce-projectbucket/bronze/transactions/"
)

display(bronze_delta)

# COMMAND ----------

bronze_delta.count()

# COMMAND ----------

display(
    dbutils.fs.ls(
        "s3://ecommerce-projectbucket/bronze/transactions/"
    )
)