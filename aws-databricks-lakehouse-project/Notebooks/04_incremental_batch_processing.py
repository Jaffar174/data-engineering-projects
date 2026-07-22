# Databricks notebook source
# MAGIC %md
# MAGIC Purpose:
# MAGIC Incrementally process new transaction batches.
# MAGIC
# MAGIC Steps:
# MAGIC 1. Read new batch file
# MAGIC 2. Append data to Bronze
# MAGIC 3. Clean and transform data
# MAGIC 4. MERGE into Silver
# MAGIC 5. Refresh Gold aggregates

# COMMAND ----------

# MAGIC %md
# MAGIC Read Batch 2

# COMMAND ----------

batch2_df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(
        "s3://ecommerce-projectbucket/raw/incoming/batch_2.csv"
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC Bronze Transformations

# COMMAND ----------

from pyspark.sql.functions import current_timestamp,to_date,col

batch2_bronze_df = (
    batch2_df
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

# MAGIC %md
# MAGIC Append to Bronze

# COMMAND ----------

(
    batch2_bronze_df.write
    .format("delta")
    .mode("append")
    .partitionBy("Transaction_Date")
    .save(
        "s3://ecommerce-projectbucket/bronze/transactions/"
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC Silver Transformations

# COMMAND ----------

from pyspark.sql.functions import (
    year,
    month,
    dayofmonth
)

incremental_df = (
    batch2_bronze_df
    .filter(col("Transaction_ID").isNotNull())
    .filter(col("Purchase_Amount") > 0)
    .dropDuplicates(["Transaction_ID"])
    .withColumn(
        "transaction_year",
        year("Transaction_Date")
    )
    .withColumn(
        "transaction_month",
        month("Transaction_Date")
    )
    .withColumn(
        "transaction_day",
        dayofmonth("Transaction_Date")
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC MERGE into Silver

# COMMAND ----------

from delta.tables import DeltaTable

silver_table = DeltaTable.forPath(
    spark,
    "s3://ecommerce-projectbucket/silver/transactions/"
)

(
    silver_table.alias("target")
    .merge(
        incremental_df.alias("source"),
        "target.Transaction_ID = source.Transaction_ID"
    )
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)

# COMMAND ----------

# MAGIC %md
# MAGIC Rebuild Gold Tables

# COMMAND ----------

silver_df = spark.read.format("delta").load(
    "s3://ecommerce-projectbucket/silver/transactions/"
)

# COMMAND ----------

# MAGIC %md
# MAGIC Check silver count

# COMMAND ----------

silver_df = spark.read.format("delta").load(
    "s3://ecommerce-projectbucket/silver/transactions/"
)

print(silver_df.count())
display(silver_df)

# COMMAND ----------

# MAGIC %md
# MAGIC Daily Sales

# COMMAND ----------

from pyspark.sql.functions import sum, count

daily_sales = (
    silver_df.groupBy("Transaction_Date")
    .agg(
        sum("Purchase_Amount").alias("total_revenue"),
        count("Transaction_ID").alias("transaction_count")
    )
)

(
    daily_sales.write
    .format("delta")
    .mode("overwrite")
    .save(
        "s3://ecommerce-projectbucket/gold/daily_sales/"
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC Country Sales

# COMMAND ----------

country_sales = (
    silver_df.groupBy("Country")
    .agg(
        sum("Purchase_Amount").alias("total_revenue"),
        count("Transaction_ID").alias("transaction_count")
    )
)

(
    country_sales.write
    .format("delta")
    .mode("overwrite")
    .save(
        "s3://ecommerce-projectbucket/gold/country_sales/"
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC Category Sales

# COMMAND ----------

category_sales = (
    silver_df.groupBy("Product_Category")
    .agg(
        sum("Purchase_Amount").alias("total_revenue"),
        count("Transaction_ID").alias("transaction_count")
    )
)

(
    category_sales.write
    .format("delta")
    .mode("overwrite")
    .save(
        "s3://ecommerce-projectbucket/gold/category_sales/"
    )
)

# COMMAND ----------

#Validate 

gold_df = spark.read.format("delta").load(
    "s3://ecommerce-projectbucket/gold/daily_sales/"
)

display(gold_df)