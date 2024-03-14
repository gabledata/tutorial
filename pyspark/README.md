# PySpark

## Prerequisites

<details>
<summary>Docker</summary>
<br>

[Link to installation page](https://docs.docker.com/engine/install/)

Once Docker is installed, try running `docker pull apache/hive:4.0.0-beta-1` to verify the Docker engine is running, and you're able to pull the image needed for the tutorial.
</details>

<details>
<summary>nvm/node</summary>
<br>


The tutorial requires NodeJS version 18 or above, which can be installed using `nvm` (Node Version Manager). To check if you already have `nvm` installed on your machine, run

```bash
nvm --version
```

If `nvm` is not installed, you can run the commands below taken from [this Medium Article](https://medium.com/devops-techable/how-to-install-nvm-node-version-manager-on-macos-with-homebrew-1bc10626181).

```bash
brew update
brew install nvm
mkdir -p ~/.nvm

echo "export NVM_DIR=~/.nvm\nsource \$(brew --prefix nvm)/nvm.sh" >> .zshrc
source ~/.zshrc
nvm --version
```

Once `nvm` is installed, you can install and use any version of node 18 or above

```bash
nvm install 18
nvm use 18
node --version
```

</details>

## Setup

From the `pyspark` folder

1. Start the hive container, which is automatically seeded with example table schemas

    ```bash
    docker-compose -f ./docker/docker-compose.yml up -d 
    ```

2. Create and activate a virtual environment, install dependencies

    The `gable` CLI requires the active Python environment to have the PySpark job's Python dependencies installed. For this tutorial, we're creating a new Python virtual environment, activating it, and installing the PySpark job's requirements which are defined in the `requirements.txt` file.

    ```bash
    python3 -m venv ".venv"
    source ".venv/bin/activate"
    pip3 install --pre -r requirements.txt
    ```

3. Set your Gable API Key

    Log into Gable, and navigate to the `Settings -> API Keys`. Copy the API endpoint & API key values, and run the following in your terminal window

    ```bash
    export GABLE_API_ENDPOINT=<copied_api_endpoint>
    export GABLE_API_KEY=<copied_api_key>
    ```

## Register PySpark Job Output Tables

Once the setup is complete, you're ready to register the PySpark job's output tables & their schemas! 

The `gable` CLI needs to know the schemas of any tables the PySpark job reads from in order to compute the final output schema(s). There are currently two methods for providing the input schemas: a connection to your Hive cluster, which allows the CLI to query the information schema, or a CSV file containing the relevant schemas.

### Hive

```bash
gable data-asset register --source-type pyspark \
  --project-root . \
  --spark-job-entrypoint "job.py --final_output_table pnw_bookings_30_days" \
  --connection-string hive://localhost:10000
```

`--project-root`: The path to the root of the Python project containing the PySpark job to run

`--spark-job-entrypoint`: The name of the entrypoint script for the PySpark job, as well as any arguments needed to run the job. If your Spar job uses config value from `SparkConf`, you can set the config values using the [normal Spark syntax](https://spark.apache.org/docs/latest/configuration.html#dynamically-loading-spark-properties) of `--conf spark.my_config_key=config_value`.

`--connection-string`: The [SQLAlchemy connection string](https://pypi.org/project/PyHive/) to connect to your Hive instance. Knowing the schemas of the SparkJob's input tables is required to compute the job's final output schemas.

### csv

```bash
gable data-asset register --source-type pyspark \
  --project-root . \
  --spark-job-entrypoint "job.py --final_output_table pnw_bookings_30_days" \
  --csv-schema-file schemas.csv
```

`--project-root`: The path to the root of the Python project containing the PySpark job to run

`--spark-job-entrypoint`: The name of the entrypoint script for the PySpark job, as well as any arguments needed to run the job. If your Spar job uses config value from `SparkConf`, you can set the config values using the [normal Spark syntax](https://spark.apache.org/docs/latest/configuration.html#dynamically-loading-spark-properties) of `--conf spark.my_config_key=config_value`.

`csv-schema-file`: A CSV file containing the schema of all tables read from the PySpark job, with the header row

*  `schema_table,col_name,col_type`
