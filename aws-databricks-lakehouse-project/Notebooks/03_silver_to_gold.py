# Databricks notebook source
silver_df = spark.read.format("delta").load(
    "s3://ecommerce-projectbucket/silver/transactions/"
)

# COMMAND ----------

# MAGIC %md
# MAGIC Gold Table 1: Daily Sales

# COMMAND ----------

from pyspark.sql.functions import sum, count

daily_sales = (
    silver_df.groupBy("Transaction_Date")
    .agg(
        sum("Purchase_Amount").alias("total_revenue"),
        count("Transaction_ID").alias("transaction_count")
    )
)

# COMMAND ----------

daily_sales.write \
    .format("delta") \
    .mode("overwrite") \
    .save(
        "s3://ecommerce-projectbucket/gold/daily_sales/"
    )

# COMMAND ----------

# MAGIC %md
# MAGIC Gold Table 2: Country Sales

# COMMAND ----------

country_sales = (
    silver_df.groupBy("Country")
    .agg(
        sum("Purchase_Amount").alias("total_revenue"),
        count("Transaction_ID").alias("transaction_count")
    )
)

# COMMAND ----------

country_sales.write \
    .format("delta") \
    .mode("overwrite") \
    .save(
        "s3://ecommerce-projectbucket/gold/country_sales/"
    )

# COMMAND ----------

# MAGIC %md
# MAGIC Gold Table 3: Category Sales

# COMMAND ----------

category_sales = (
    silver_df.groupBy("Product_Category")
    .agg(
        sum("Purchase_Amount").alias("total_revenue"),
        count("Transaction_ID").alias("transaction_count")
    )
)

# COMMAND ----------

category_sales.write \
    .format("delta") \
    .mode("overwrite") \
    .save(
        "s3://ecommerce-projectbucket/gold/category_sales/"
    )

# COMMAND ----------

# MAGIC %md
# MAGIC Validate Gold

# COMMAND ----------

gold_df = spark.read.format("delta").load(
    "s3://ecommerce-projectbucket/gold/daily_sales/"
)

display(gold_df)