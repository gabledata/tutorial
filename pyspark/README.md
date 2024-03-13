# PySpark

## Setup

From the `pyspark` folder

1. Start the hive container, which is automatically seeded with example table schemas

    ```bash
    docker-compose -f ./docker/docker-compose.yml up -d 
    ```

2. Create and activate a virtual environment, install dependencies

    ```bash
    python3 -m venv ".venv"
    source ".venv/bin/activate"
    pip3 install --pre -r requirements.txt
    ```

## Register PySpark Job Output Tables

To register the PySpark job's output tables & their schemas, run the following command

```bash
gable data-asset register --source-type pyspark \
  --project-root . \
  --spark-job-entrypoint "job.py --final_output_table pnw_bookings_30_days" \
  --connection-string hive://localhost:10000
```

`--project-root`: The path to the root of the Python project containing the PySpark job to run

`--spark-job-entrypoint`: The name of the entrypoint script for the PySpark job, as well as any arguments needed to run the job. If your Spar job uses config value from `SparkConf`, you can set the config values using the [normal Spark syntax](https://spark.apache.org/docs/latest/configuration.html#dynamically-loading-spark-properties) of `--conf spark.my_config_key=config_value`.

`--connection-string`: The [SQLAlchemy connection string](https://pypi.org/project/PyHive/) to connect to your Hive instance. Knowing the schemas of the SparkJob's input tables is required to compute the job's final output schemas.
