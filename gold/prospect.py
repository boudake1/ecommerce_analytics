from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def prospect_user(spark: SparkSession,silver_path: str) -> DataFrame:
        # Load silver layer datasets
    events_df = spark.read.parquet(f"{silver_path}/events")

    w_user_time = Window.partitionBy("user_id").orderBy("timestamp2")
    df = events_df.withColumn(
    "cumulative_spend", F.sum("price").over(w_user_time)
       ).withColumn(
    "prev_event_time", F.lag("timestamp2", 1).over(w_user_time)
      ).withColumn(
    "hours_since_last_event",
    (F.unix_timestamp("timestamp2") - F.unix_timestamp("prev_event_time")) / 3600
     )
    return df.select(
        "user_id",
        "price",
        "prev_event_time",
        "cumulative_spend",
        "hours_since_last_event"   )