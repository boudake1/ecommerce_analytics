from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window

def build_customer_360(spark: SparkSession,silver_path: str) -> DataFrame:
    # Load silver layer datasets
    events_df = spark.read.parquet(f"{silver_path}/events")
    customers_df = spark.read.parquet(f"{silver_path}/customers")
    products_df = spark.read.parquet(f"{silver_path}/products")
    
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


def customerFavoriteProduct(spark: SparkSession,silver_path: str) -> DataFrame:
    # Load silver layer datasets
    events_df = spark.read.parquet(f"{silver_path}/events")
    customers_df = spark.read.parquet(f"{silver_path}/customers")

    window_spec = Window.partitionBy("user_id")
    window_spec_user_product = Window.partitionBy("user_id", "product_id")
    customer_purchases = (
        events_df
        .filter(F.col("event_type") == "purchase")
        .withColumn("prev_amount", F.lag("amount").over(window_spec))
        .withColumn("next_amount", F.lead("amount").over(window_spec))
        .withColumn("purchase_count", F.count("*").over(window_spec_user_product))
    )
    
    # Join with customers table
    favortiteProduct = (
        customers_df
        .join(customer_purchases, F.col("user_id") == F.col("user_id"), "left_outer")
        .select(
            F.col("user_id").alias("customer_id"),
            F.col("name"),
            F.col("prev_amount"),
            F.col("next_amount"),
            F.col("purchase_count")
        )
    )
    
    return favortiteProduct