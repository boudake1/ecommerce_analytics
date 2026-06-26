from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def build_category_performance(spark: SparkSession,silver_path: str) -> DataFrame:

    events_df = spark.read.parquet(f"{silver_path}/events")
    product_df = spark.read.parquet(f"{silver_path}/products")
    
    category_window = Window.partitionBy("categoryName")


    category_performance = (
        events_df
            .join(product_df.withColumnRenamed("product_id", "product_id_from_events"), F.col("product_id") == F.col("product_id_from_events"), "inner")
            .withColumn("purchase_count",
                F.sum(
                    F.when(F.col("event_type").isin("purchase"), F.lit(1))
                    .otherwise(F.lit(0))
                ).over(category_window)
            ).withColumn("total_spent",
                F.sum(
                    F.when(F.col("event_type").isin("purchase"), F.col("price"))
                    .otherwise(F.lit(0))
                ).over(category_window)
            ).withColumn("average_spent",
                F.avg(
                    F.when(F.col("event_type").isin("purchase"), F.col("price"))
                    .otherwise(F.lit(0))
                ).over(category_window)
            ).withColumn("first_purchase_date",
                F.min(
                    F.when(F.col("event_type").isin("purchase"), F.col("timestamp"))
                    .otherwise(F.lit(0))
                ).over(category_window)
            ).withColumn("last_purchase_date",
                F.max(
                    F.when(F.col("event_type").isin("purchase"), F.col("timestamp"))
                    .otherwise(F.lit(0))
                ).over(category_window)
            ).withColumn("add_to_cart_count",   
                F.sum(
                    F.when(F.col("event_type").isin("add_to_cart"), F.lit(1))
                    .otherwise(F.lit(0))
                ).over(category_window)

            ).withColumn("view_count",   
                F.sum(
                    F.when(F.col("event_type").isin("product_view"), F.lit(1))
                    .otherwise(F.lit(0))
                ).over(category_window)
            ).dropDuplicates(["categoryName"])
            
            .select(
                F.col("categoryName"),
                F.col("purchase_count"),
                F.col("total_spent"),
                F.col("view_count"),
                F.col("add_to_cart_count")
            )
    )
    return category_performance