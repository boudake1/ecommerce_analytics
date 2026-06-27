
from pyspark.sql.functions import to_timestamp, col
def clean_events(df):

    return (
        df
        .withColumn("timestamp2", to_timestamp(col("timestamp"), "yyyy-MM-dd'T'HH:mm:ss.SSSSSS"))
        .dropDuplicates(["event_id"])
    )