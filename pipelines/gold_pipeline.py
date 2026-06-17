from gold.registry import AGGREGATIONS

class GoldPipeline:

    def __init__(self, spark, config):
        self.spark = spark
        self.config = config
    
    def load_silver(self, dataset):
        silver_path = self.config.get("paths").get("silver")
        return self.spark.read.parquet(f"{silver_path}/{dataset}")

    def aggregate(self, aggregation):
        aggregation_func = AGGREGATIONS.get(aggregation)
        if not aggregation_func:
            raise ValueError(f"Aggregation function not found for dataset: {aggregation}")
        return aggregation_func(self.spark)
    
    def save_gold(self, df, aggregation):
        gold_path = self.config.get("paths").get("gold")
        df.write.mode("overwrite").parquet(f"{gold_path}/{aggregation}")

    def run(self):
        for aggregation in self.config.get("agregations"):
            print(f"Running aggregation: {aggregation}")
            gold_df = self.aggregate(aggregation)
            self.save_gold(gold_df, aggregation)
            gold_df.show(10, False)
            print(gold_df.count())