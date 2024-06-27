import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

from script import run_job

def parse_arguments(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--final_output_table")
    return ap.parse_args(argv)


if __name__ == "__main__":
    # Parse args
    args_main = parse_arguments()
    final_output_table = args_main.final_output_table
    print(f"final_output_table: {final_output_table}")
    
    spark = SparkSession.builder.getOrCreate()
    run_job(spark, final_output_table)
    
