from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, concat, rand, floor, explode, array

spark = SparkSession.builder.appName("SaltingExample").getOrCreate()

# A massive dataframe where "Store_101" is heavily skewed
large_data = [("Store_101", i) for i in range(1000000)] + [("Store_102", 1), ("Store_103", 2)]
large_df = spark.createDataFrame(large_data, ["store_id", "amount"])

salt_bins = 5  # Number of splits we want for the skewed key

# Add a salted key column: e.g., "Store_101_2"
salted_large_df = large_df.withColumn(
    "salted_key", 
    concat(col("store_id"), lit("_"), floor(rand() * salt_bins))
)

salted_large_df.show(20)

small_data = [("Store_101", "New York"), ("Store_102", "Los Angeles"), ("Store_103", "Chicago")]
small_df = spark.createDataFrame(small_data, ["store_id", "location"])

# Create an array of strings [0, 1, 2, 3, 4]
salt_array = [lit(i) for i in range(salt_bins)]

# Explode the small dataframe so every store has 5 variations
replicated_small_df = small_df.withColumn("salt", explode(array(salt_array))) \
                              .withColumn("salted_key", concat(col("store_id"), lit("_"), col("salt")))

replicated_small_df.show(10)
# Join on the salted key
final_df = salted_large_df.join(
    replicated_small_df, 
    on="salted_key", 
    how="inner"
).drop("salted_key", "salt") # Clean up the salt columns afterward

final_df.show(5)