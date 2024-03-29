from script import run_job

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

if __name__ == "__main__":
    final_output_table = "pnw_bookings_30_days"
    print(f"final_output_table: {final_output_table}")
    
    spark = SparkSession.builder.getOrCreate()
    run_job(spark, final_output_table)
    
