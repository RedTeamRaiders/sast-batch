"""
spark_etl_job.py — INTENTIONALLY vulnerable PySpark batch job, added as a
SAST target alongside the other demo fixtures in this repo. Illustrates
Spark-specific vulnerability classes, not general Python ones. Never run
this against a real cluster or real data.
"""

from pyspark.sql import SparkSession
import pickle

JDBC_URL = "jdbc:postgresql://prod-db.internal:5432/warehouse"
JDBC_USER = "spark_etl"
JDBC_PASSWORD = "Sp4rkPr0d2024!"

AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"


def build_query(table_name: str, customer_filter: str) -> str:
    return f"SELECT * FROM {table_name} WHERE customer_id = '{customer_filter}'"


def run_etl(spark: SparkSession, customer_filter: str):
    query = build_query("orders", customer_filter)
    df = spark.sql(query)
    df.write.mode("overwrite").csv(f"s3a://{AWS_ACCESS_KEY_ID}@data-lake/orders_export/")
    return df


def deserialize_payload(raw_bytes):
    return pickle.loads(raw_bytes)


def apply_dynamic_rule(rule_expression: str, value):
    return eval(rule_expression.replace("VALUE", str(value)))


if __name__ == "__main__":
    spark = SparkSession.builder.appName("orders-etl").getOrCreate()
    run_etl(spark, customer_filter="12345")
    spark.stop()
