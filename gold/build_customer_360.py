from pyspark.sql import SparkSession
from pyspark.sql import functions as F

def build_customer_360(spark: SparkSession) -> DataFrame:
    # Load silver layer datasets
    events_df = spark.read.parquet("data/silver/events")
    customers_df = spark.read.parquet("data/silver/customers")
    products_df = spark.read.parquet("data/silver/products")
    
    # For this example, we assume 'events' contains purchase information
    # and 'products' contains product categories
    # We join customers with their purchases and calculate aggregated metrics
    
    # Aggregate purchase data by customer
    today_date = F.current_date()
    customer_purchases = (
        events_df
        .filter(F.col("event_type") == "purchase")
        .groupBy("user_id")
        .agg(
            F.count("*").alias("purchase_count"),
            F.sum("price").alias("total_spent"),
            F.avg("price").alias("average_spent"),
            F.min("timestamp").alias("first_purchase_date"),
            F.max("timestamp").alias("last_purchase_date")
        )
        .withColumn("days_since_last_purchase", today_date - F.col("last_purchase_date"))
        .withColumn("days_since_first_purchase", today_date - F.col("first_purchase_date"))
    )
    
    # Join with customers table
    customer_360 = (
        customers_df
        .join(customer_purchases, F.col("user_id") == F.col("user_id"), "left_outer")
        .select(
            F.col("user_id").alias("customer_id"),
            F.col("purchase_count"),
            F.col("total_spent"),
            F.col("first_purchase_date"),
            F.col("days_since_first_purchase"),
            F.col("last_purchase_date")
        )
    )
    
    return customer_360