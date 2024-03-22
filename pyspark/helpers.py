from pyspark.sql.session import SparkSession
from pyspark.sql.functions import col, concat, lit, floor, rand
from pyspark.sql import functions as F

def get_cities_by_region(spark,region):
  region_cities_df = (
    spark.table("city")
    .select(
        "city_id",
        "city_name",
        "city_code",
        "country_id",
        "region",
        "created_at",
        "enable_tip"
    )
    .filter('region="{}"'.format(region))
  )
  return region_cities_df