from pyspark.sql import SparkSession
import sys
from config.settings import load_config
from pipelines.bronze_pipeline import BronzePipeline
from pipelines.silver_pipeline import SilverPipeline
# from ingestion.log_generator import generate_fake_events_json
from config.config import Config
from pipelines.gold_pipeline import GoldPipeline
from delta import configure_spark_with_delta_pip

def main(config_file: str):
# Create Spark session
     config = Config(config_file)
     builder = SparkSession.builder \
         .appName("EcommerceAnalytics") \
         .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
         .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") 
         #.getOrCreate()
     spark = configure_spark_with_delta_pip(builder).getOrCreate()
# appConfig = load_config("config/config.json")
#     spark.sparkContext.setLogLevel("error")

     bronze_pipeline = BronzePipeline(spark, config)
     bronze_pipeline.run()
     silver_pipeline = SilverPipeline(spark, config)
     silver_pipeline.run()
     gold_pipeline = GoldPipeline(spark, config)
     gold_pipeline.run()
#    spark.stop()

if __name__ == "__main__":
     config_file = sys.argv[1]
     main(config_file)













    