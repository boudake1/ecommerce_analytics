from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def build_product_performance(spark: SparkSession) -> DataFrame:
    events_df = spark.read.parquet("data/silver/events")
    product_df = spark.read.parquet("data/silver/products")
    
    product_window = Window.partitionBy("product_id")

    customer_purchases = (
        events_df
            .withColumn("score",  F.when(F.col("event_type") == "purchase", F.lit(20))
                                    .when(F.col("event_type") == "add_to_cart", F.lit(10))
                                    .when(F.col("event_type") == "product_view", F.lit(5))
                                    .otherwise(F.lit(0)))
            .withColumn("score_sum",  F.sum("score").over(product_window))                        
            .withColumn("purchase_count",
                F.sum(
                    F.when(F.col("event_type").isin("purchase"), F.lit(1))
                    .otherwise(F.lit(0))
                ).over(product_window)
            ).withColumn("total_spent",
                F.sum(
                    F.when(F.col("event_type").isin("purchase"), F.col("price"))
                    .otherwise(F.lit(0))
                ).over(product_window)
            ).withColumn("average_spent",
                F.avg(
                    F.when(F.col("event_type").isin("purchase"), F.col("price"))
                    .otherwise(F.lit(0))
                ).over(product_window)
            ).withColumn("first_purchase_date",
                F.min(
                    F.when(F.col("event_type").isin("purchase"), F.col("timestamp"))
                    .otherwise(F.lit(0))
                ).over(product_window)
            ).withColumn("last_purchase_date",
                F.max(
                    F.when(F.col("event_type").isin("purchase"), F.col("timestamp"))
                    .otherwise(F.lit(0))
                ).over(product_window)
            ).withColumn("add_to_cart_count",   
                F.sum(
                    F.when(F.col("event_type").isin("add_to_cart"), F.lit(1))
                    .otherwise(F.lit(0))
                ).over(product_window)

            ).withColumn("add_to_cart_count",   
                F.sum(
                    F.when(F.col("event_type").isin("add_to_cart"), F.lit(1))
                    .otherwise(F.lit(0))
                ).over(product_window)
            ).withColumn("view_count",   
                F.sum(
                    F.when(F.col("event_type").isin("product_view"), F.lit(1))
                    .otherwise(F.lit(0))
                ).over(product_window)
            ).dropDuplicates(["product_id"])
            .withColumnRenamed("product_id", "product_id_from_events")
    )

      
    customer_views = (
        events_df
            .filter(F.col("event_type") == "product_view")
            .groupBy("product_id")
            .agg(
                F.count("*").alias("view_count"),
                F.min("timestamp").alias("first_view_date"),
                F.max("timestamp").alias("last_view_date")
            )
            .withColumnRenamed("product_id", "product_id_from_events")
    )
    product_performance = (
        product_df
            .join(customer_purchases, F.col("product_id") == F.col("product_id_from_events"), "left_outer")
            .select(
                F.col("product_id"),
                F.col("purchase_count"),
                F.col("total_spent"),
                F.col("view_count"),
                F.col("add_to_cart_count"),
                F.col("score_sum")
            )
    )
    return product_performance