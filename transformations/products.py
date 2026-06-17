from pyspark.sql.functions import col, lit, date_format, lower, when, concat_ws, current_timestamp

def normalize_products(df):
    """
    Transform product data to a normalized format.
    """
    # Ensure product_id is a string
    df = df.withColumn("product_id", col("product_id").cast("string"))
    
    # Convert category and subcategory to lowercase
    df = df.withColumn("categoryName", lower(col("categoryName")))
    df = df.withColumnRenamed("name", "product_name")



    # Select and reorder columns to a normalized structure
    normalized_df = df.select(
        col("product_id"),
        col("categoryName"),
        col("product_name")
    )
    
    return normalized_df