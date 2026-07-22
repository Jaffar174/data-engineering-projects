# Databricks notebook source
bronze_df = spark.read.format("delta").load(
"s3://ecommerce-projectbucket/bronze/transactions/"
)

# COMMAND ----------

from pyspark.sql.functions import col

silver_df = bronze_df.filter(
    col("Transaction_ID").isNotNull()
)

# COMMAND ----------

silver_df = silver_df.filter(
    col("Purchase_Amount") > 0
)

# COMMAND ----------

silver_df = silver_df.dropDuplicates(
    ["Transaction_ID"]
)

# COMMAND ----------

from pyspark.sql.functions import year
from pyspark.sql.functions import month
from pyspark.sql.functions import dayofmonth

silver_df = (
    silver_df
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

silver_df.write \
    .format("delta") \
    .mode("overwrite") \
    .save(
        "s3://ecommerce-projectbucket/silver/transactions/"
    )

# COMMAND ----------

silver_check = spark.read.format("delta").load(
    "s3://ecommerce-projectbucket/silver/transactions/"
)

silver_check.count()

# COMMAND ----------

silver_df = spark.read.format("delta").load(
    "s3://ecommerce-projectbucket/silver/transactions/"
)

# COMMAND ----------

# MAGIC %md
# MAGIC Check Duplicates

# COMMAND ----------

from pyspark.sql.functions import count

silver_df.groupBy("Transaction_ID") \
         .count() \
         .filter("count > 1") \
         .count()

# COMMAND ----------

# MAGIC %md
# MAGIC Check for null transaction ids

# COMMAND ----------

silver_df.filter(
    silver_df.Transaction_ID.isNull()
).count()

# COMMAND ----------

# MAGIC %md
# MAGIC Validate the derived columns

# COMMAND ----------

silver_df.select(
    "Transaction_Date",
    "transaction_year",
    "transaction_month",
    "transaction_day"
).show(5)