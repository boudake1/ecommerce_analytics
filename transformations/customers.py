from pyspark.sql.functions import col, lit, date_format, lower, when, concat_ws, current_timestamp

def normalize_customers(df):
    """
    Transform customer data to a normalized format suitable for analytical queries.
    """
    # Rename user_id to customer_id for consistency
    df = df.withColumnRenamed("user_id", "customer_id")
    
    # Normalize email column (convert to lowercase)
    df = df.withColumn("email", lower(col("email"))) 
    
    # Standardize gender column: 'F' -> 'Female', 'M' -> 'Male'
    df = df.withColumn("gender", 
        when(col("gender") == "F", "Female")
        .when(col("gender") == "M", "Male")
        .otherwise(col("gender"))
    )

    # Ensure age is a numeric type (integer)
    df = df.withColumn("email", lower("email"))
    
    # Standardize address format: add commas between street, city, state, zip
    df = df.withColumn("address_normalized", 
        concat_ws(", ", 
            col("address"),
            col("city"),
            col("state"),
            col("zip_code")
        )
    )
    
    # Add metadata columns
    df = df.withColumn("updated_at", current_timestamp())
    
    # Select and reorder columns to a normalized structure
    normalized_df = df.select(
        col("customer_id"),
        col("name"),
        col("email"),
        col("age"),
        col("gender"),
        col("address"),
        col("city"),
        col("state"),
        col("zip_code"),
        col("address_normalized"),
        col("updated_at")
    )
    
    return normalized_df