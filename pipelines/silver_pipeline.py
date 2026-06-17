from pyspark.sql.functions import col
from transformations.registry import TRANSFORMATIONS

class SilverPipeline:

    def __init__(self, spark, config):
        self.spark = spark
        self.config = config

    def load_bronze(self, dataset):
        """Load dataset from bronze layer"""
        bronze_path = self.config.get("paths").get("bronze")
        return self.spark.read.parquet(f"{bronze_path}/{dataset}")
    
    def save_silver(self, df, dataset):
        """Save dataset to silver layer"""
        silver_path = self.config.get("paths").get("silver")
        df.write.mode("overwrite").parquet(f"{silver_path}/{dataset}")

    def clean_data(self, bronze_df, dataset):
        transformer = TRANSFORMATIONS[dataset]
        clean_df = transformer(bronze_df)
        return clean_df

    def run(self):
        datasets = self.config.get("datasets")
        for dataset in datasets:
            df = self.load_bronze(dataset)
            silver_df = self.clean_data(df, dataset)
            self.save_silver(silver_df, dataset)