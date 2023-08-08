# Tutorial: Getting Started with Gable Platform

Welcome to the tutorial for Gable! In this tutorial, you will:

- Set up a local environment to connect to Gable's platform
- Register Protobuf and Avro files as Data Assets in Gable's platform
- Publish data contracts for a Protobuf and an Avro file
- Check to ensure that the data assets to not violate the data contract

## Step 1: Set up Gable CLI

Gable uses a Python-based CLI to interact with the Gable API. The Gable CLI requires a Python environment running at least Python 3.10.

### Clone this tutorial repository

The first step is to clone this tutorial repository onto your local machine. Open a terminal and run:

```bash
git clone https://github.com/gabledata/tutorial.git
cd tutorial
```

### Recommended: Create and Activate Virtual Environment

For this tutorial, it is recommended you install Gable into a virtual environment. This will keep the current installation of the Gable CLI separate from any other Python environments on your local machine. To create a virtual environment, open your terminal and run:

```bash
python3 -m venv gable_tutorial
```

This will create a virtual environment called `gable_tutorial`. To activate the environment, run:

```bash
source gable_tutorial/bin/activate
```

### Install CLI Download

Gable's CLI is hosted on PyPi and can be installed with any Python package manager like `pip`. To install the Gable CLI with pip, run:

```bash
pip install gable
```

### Get Your API Key

To establish an authenticated connection with Gable via the CLI, you need:

- The API endpoint associated with your organization
- An API key that corresponds to the endpoint

You can find your API key by navigating to the `/settings` page of Gable. Under API Keys you can click `View` to reveal your API key.

![Gable API Keys](./static/gable_settings_api_keys_page_example.png)

### Set ENV variables

In order to pass your API endpoint and API Key to the Gable CLI, you should set them as environment variables. For the purposes of this tutorial, you can simply run the following command in your terminal:

```bash
export GABLE_API_ENDPOINT="https://api.yourorganization.gable.ai"
export GABLE_API_KEY="yourapikey"
```

Make sure to replace `youorganization` with your provided organization name and `yourapikey` with your actual API key from the previous step.

### Check connection

To confirm that everything is working, run the following command:

```bash
gable ping
```

If everything is set up correctly, you should receive a success message confirming the connection.

## Step 2: Registering Data Assets

Included in this tutorial are two Protobuf files and one Avro file which we will register as data assets.

1. First, register the two Protobuf files with the following command:

   ```bash
   gable data-asset register --source-type protobuf \
       --files ./event_schemas/*.proto
   ```

   This command will register and files with a `proto` extension in the `event_schemas` directory. This command is idempotent so running it multiple times will not duplicate data assets.

   If successful, you will receive a message with the ids of the registered Protobuf data assets.

2. Register the Avro schema by running the following command:

   ```bash
   gable data-asset register --source-type avro \
       --files ./event_schemas/*.avsc
   ```

   This command will register and files with a `avsc` extension in the `event_schemas` directory.

3. To get a list of all of your registered data assets, run:

   ```bash
   gable data-asset list
   ```

## Step 3: Publish the Data Contract

1. Before you register the data contract in Gable's platform, you first want to validate that the data contract is syntactically correct. Run:

   ```bash
   gable contract validate ./contracts/*.yaml
   ```

   This command will validate any files with a `yaml` extension in the `contracts` directory to confirm they are valid data contracts.

2. To publish the data contract with Gable CLI, run:

   ```bash
   gable contract publish ./contracts/*.yaml
   ```

   This command will publish any files with a `yaml` extension in the `contracts` directory to the Gable platform. This command is idempotent so running it multiple times will not duplicate data contracts. It will only register new versions of the data contract if there are changes.

   If successful, you will receive a message with the ids of the published data contracts.

3. Check back in the UI and you should see your two data contracts listed.

## Step 4: Checking the Data

The last step is to ensure

1. First, check to ensure that your current Protobuf data assets are compliant with the published data contract by running:

   ```bash
   gable data-asset check \
       --source-type protobuf --files ./event_schemas/*.proto
   ```

   The CLI will surface a warning for any data assets not under contract. For any data assets under contract, in this case `VehicleLocation.proto`, it should return a success message that the data asset is not in violation of its contract.

2. Confirm that the Avro file is also in complaince by running:

   ```bash
   gable data-asset check \
       --source-type avro --files ./event_schemas/*.avsc
   ```

3. Modify the `VehicleLocation.proto` file by changing the `status` column to `vehicleStatus`. This renames a field that is under the data contract and will result in a violation of the contract.

4. Rerun the Protobuf check

   ```bash
   gable data-asset check \
       --source-type protobuf --files ./event_schemas/*.proto
   ```

   As expected, the data asset is failing the check because it is in violation of the contract!


Congratulations for creating your first data contracts! Be sure to check out more of [Gable's documentation](https://docs.gable.ai) for more information on our platform!