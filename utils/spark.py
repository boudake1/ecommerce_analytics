from pyspark.sql import SparkSession

def read_from_jdbc(
    spark: SparkSession,
    url: str,
    table: str,
    user: str,
    password: str,
    driver: str = "org.postgresql.Driver"
):
    """
    Generic function to read any table from a JDBC source into a Spark DataFrame.
    """
    df = spark.read.format("jdbc") \
        .option("url", url) \
        .option("dbtable", table) \
        .option("user", user) \
        .option("password", password) \
        .option("driver", driver) \
        .load()
    return df

def read_from_json(spark, path, format="json"):
    """
    Generic function to read any file from JSON into a Spark DataFrame.
    """
    df = spark.read.format(format).load(path)
    return df   

def read_from_csv(spark, path, format="csv"):
    """
    Generic function to read any file from S3 into a Spark DataFrame.
    """
    df = spark.read.format(format).load(path)
    return df   
    