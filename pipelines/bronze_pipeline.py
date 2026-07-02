from transformations.registry import TRANSFORMATIONS


class BronzePipeline:

    def __init__(self, spark, config):
        self.spark = spark
        self.config = config
    
    def load(self, dataset):
        """Load dataset from raw files"""
        raw_path = self.config.get("paths").get("raw")
        return self.spark.read.json(
            f"{raw_path}/{dataset}.json"
        )
    
    def save(self, dataset, df, mode="overwrite"):
        """Save dataset to bronze layer"""
        bronze_path = self.config.get("paths").get("bronze")
        (
            df.write
            .mode(mode)
            .parquet(
                f"{bronze_path}/{dataset}"
            )
        )

    def saveDelta(self, dataset, df):
        """Save dataset to bronze layer in Delta format"""
        bronze_path = self.config.get("delta_paths").get("bronze")
        (
            df.write
            .format("delta")
            .mode("overwrite")
            .save(
                f"{bronze_path}/{dataset}"
            )
        )

    def saveDeltaAsTable(self, dataset, df):
        """Save dataset to bronze layer in Delta format"""
        (
            df.write
            .format("delta")
            .mode("overwrite")
            .saveAsTable(
                f"bronze.{dataset}"
            )
        )    

    def run(self):
        """Run the bronze pipeline"""
        datasets = self.config.get("datasets")
        for dataset in datasets:
            df = self.load(dataset)
            self.save(dataset, df)
            self.saveDelta(dataset, df)
            self.saveDeltaAsTable(dataset, df)