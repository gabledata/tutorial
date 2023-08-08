# Tutorial: Getting Started with Gable Platform

Welcome to the tutorial for Gable! In this tutorial, you will:

- Set up a forked tutorial repository with Gable and Github Actions
- Validate and publish a new data contract
- Attempt to modify a data asset under contract

This tutorial utilizes Github Actions to validate and publish data contracts and register and check data assets with the Gable platform. If you would like to run a similar tutorial using just the CLI, we have that tutorial for you.

## Step 1: Set up a forked tutorial repository

### Fork this repository into your account

Navigate to the [tutorial repository](https://github.com/gabledata/tutorial) and click on the "Fork" button in the top-right corner of the repository's page.

![Fork Tutorial Repo](./static/gable_fork_tutorial.png)

A dialog may appear, asking you where to fork the repository (if you're part of any organizations). Choose your personal account (or the desired organization) to create the fork.

After clicking the create button, wait a moment as GitHub creates a copy of the repository under your account.

### Get Your API Key

In order to connect the Github Actions to Gable, you need:

- The API endpoint associated with your organization
- An API key that corresponds to the endpoint

You can find your API key by navigating to the `/settings` page of Gable. Under API Keys you can click `View` to reveal your API key.

![Gable API Keys](./static/gable_settings_api_keys_page_example.png)

### Setting up GABLE_API_KEY and GABLE_API_ENDPOINT secrets

You will need to create the `GABLE_API_KEY` and `GABLE_API_ENDPOINT` secrets in your repository settings to configure Github Actions to talk to Gable.

1. Navigate to the main page of your forked tutorial repository in Github
2. Click on the "Settings" tab near the top-right corner of the page
3. In the left-hand menu, scroll down and click on the "Secrets & security" section
4. Click on "Actions" under the "Secrets" heading
5. Click the "New repository secret" button
6. In the "Name" field, type `GABLE_API_KEY`. This is the key for the API Key secret.
7. In the "Value" field, paste the API Key from the UI
8. Click the "Add secret" button to save the secret
9. Repeat steps 6 through 8 for the `GABLE_API_ENDPOINT`

### Clone the forked tutorial repository

The last setup step is to clone the forked repository to your local machine. Navigate to the main page of the forked repository within your GitHub account and click the "Code" button and copy either the HTTPS or SSH url for the repository.

Now open a terminal and run:

```bash
git clone COPIED_REPO_URL
cd tutorial
```

Congratulations! You've set up your tutorial repository and are ready to try out Gable's platform!

## Step 2: Creating Your First Data Contract

The tutorial repository includes three data asset files for a fake public transit agency. The data assets are two Protobuf files and one Avro file which handle different aspects of the data for the public transit agency.

### Create a new branch to add the contract

You are going to create a new data contract in the tutorial repository. Rather than creating the contract in the `main` branch of the repository, it is best practice to use branches and then make a Pull Request to merge the changes in. The PR allows others to comment on your changes and also allows the Github Actions to validate the contract is syntactically correct before pushing changes.

You can either create a new branch using the Github web interface or using the git command line tools. This tutorial will walk through creating the branch using the git command line. In the tutorial repository on your local machine:

1. **Open a Terminal Window**: Navigate to the directory where your cloned tutorial repository is located
2. **Checkout a New Branch**: Use the following command to create and switch to a new branch called `first_contract`:

   ```bash
   git checkout -b first_contract
   ```

3. **Push the New Branch to GitHub**: To make this branch available on GitHub, you need to push it. Use the following command:

   ```bash
   git push origin first_contract
   ```

4. **Set the Upstream Branch**: You will want to set this new branch as the tracking branch. To do this, run:

   ```bash
   git branch --set-upstream-to=origin/first_contract
   ```

Great! Now you can start writing the contract!

### Write the data contract

You are going to create a data contract for teh `VehicleLocation.proto` file which handles data reporting the location and status of a vehicle in the transit agency. Writing a data contract involves creating a YAML file that declares the schema and semantics of the data following the [data contract specification](https://docs.gable.ai/data_contracts/what_are_data_contracts/data_contract_spec).

In the `contracts` directory of your local repository, create a file called `vehicle_location.yaml`. Copy and paste the following into the contents of that file:

```yaml
id: 6b7f4f6c-324c-4a26-9114-eefdee49d5c9
dataAssetResourceName: protobuf://git@github.com:gabledata/event_schemas/VehicleLocation.proto:transit.VehicleLocationEvent
spec-version: 0.1.0
name: VehicleLocationEvent
namespace: Transit
doc: Real-time location and status of a transit vehicle
owner: Chad Gable
schema:
  - name: agencyId
    doc: The ID of the transit agency that operates this route.
    type: string32
  - name: vehicleId
    doc: The identifier of the specific vehicle
    type: string32
  - name: timestamp
    doc: Epoch timestamp of the vehicle location
    type: int64
  - name: latitude
    doc: The latitude of the vehicle location
    type: float32
  - name: longitude
    doc: The longitude of the vehicle location
    type: float32
  - name: status
    doc: Status of the vehicle at the time of the location update
    type: string32
```

This contract contains information on what data the contract applies to, who owns the contract, as well as the minimum expected schema for the data from the `VehicleLocationEvent`.

### Push Your Changes to Github

Now that you have created the contract, it is time to commit the change to the repository. To stage and commit your changes, run:

```bash
git add .
git commit -m "Added vehicle location data contract"
git push
```

### Validate the data contract

Before merging your changes back to the `main` branch, it is a good idea to create a Pull Request. Creating the Pull Request will serve two purposes:

- Allow others to review your newly-created data contract
- Allow the Github Action to validate the data contract is syntactically correct

To create the Pull Request:

1. Navigate to the main page of your forked tutorial repository in Github
2. Click on the "Pull requests" tab near the top of the page
3. Click the "New Pull Request" button
4. In the "base" dropdown, select the `main` branch
5. In the "compare" dropdown, select the `first_contract` branch that contains your new data contract
6. In the "Title" field, add `New VehicleLocationEvent Data Contract`
7. In the "Leave a comment" field, add the following:

   ```
   Adds a new data contract for the `VehicleLocationEvent` data.
   ```

8. Click the "Create Pull Request" button.

### Publish the Data Contract

Merge the Pull Request you opened. This will

Once the Github Action on the main branch has been run and the data contract has been published, navigate to the Gable UI and you should see your new data contract!

## Step 3: Preventing Breaking Data Changes

**NOTE**: This section relies on the `VehicleLocationEvent` data contract created in the previous step. Please complete that step if you have not already.

Now that there is a data contract in place for the `VehicleLocationEvent` data, every time a change is made to the data asset, Gable checks to ensure that changes do not violate the contract. In this section, you will attempt to make a breaking change to the `VehicleLocationEvent` data.

### Create a new branch

First off, pull changes down from the main branch to ensure that your repository is up-to-date. Create a new branch called `breaking_data_change`:

```bash
git checkout main
git pull
git checkout -b breaking_data_change
```

### Make a Breaking Change

Modify the `VehicleLocation.proto` file by changing the `status` column to `vehicleStatus`. This renames a field that is protected in the data contract and will result in a violation of the contract.

Once the change has been saved, commit the change and push it to Github:

```bash
git add .
git commit -m "Rename VehicleLocationEvent status field"
git push
```

### Open a Pull Request

Now open a Pull Request for the proposed breaking change:

1. Navigate to the main page of your forked tutorial repository in Github
2. Click on the "Pull requests" tab near the top of the page
3. Click the "New Pull Request" button
4. In the "base" dropdown, select the `main` branch
5. In the "compare" dropdown, select the `breaking_data_change` branch that contains the breaking data change
6. In the "Title" field, add `Rename status field in VehicleLocationEvent Data`
7. In the "Leave a comment" field, add the following:

   ```
   Rename the `status` field to `vehicleStatus` in `VehicleLocationEvent` data.
   ```

8. Click the "Create Pull Request" button.

### View Warning Message

The Github Action will validate the changes against existing data contracts. It will detect the change to the `VehicleLocationEvent` schema and post a message in the PR that this change breaks the existing data contract.

## Further Reading

Congratulations on creating your first data contract and validating data asset changes! Be sure to check out more of [Gable's documentation](https://docs.gable.ai) for more information on our platform!
