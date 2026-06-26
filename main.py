from pyspark.sql import SparkSession
import sys
from config.settings import load_config
from pipelines.bronze_pipeline import BronzePipeline
from pipelines.silver_pipeline import SilverPipeline
# from ingestion.log_generator import generate_fake_events_json
from config.config import Config
from pipelines.gold_pipeline import GoldPipeline

def main(config_file: str):
# Create Spark session
     config = Config(config_file)
     spark = SparkSession.builder \
         .appName("EcommerceAnalytics") \
         .getOrCreate()
    
     appConfig = load_config("config/config.json")
#     spark.sparkContext.setLogLevel("error")

     bronze_pipeline = BronzePipeline(spark, config)
     bronze_pipeline.run()
     silver_pipeline = SilverPipeline(spark, config)
     silver_pipeline.run()
     gold_pipeline = GoldPipeline(spark, config)
     gold_pipeline.run()
     spark.stop()

if __name__ == "__main__":
     config_file = sys.argv[1]
     main(config_file)

# if __name__ == "__main__":
#     print("This is a placeholder for the main application logic. Please implement the main function to run the pipelines.")         














    