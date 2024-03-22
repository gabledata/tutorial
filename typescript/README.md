# TypeScript Tutorial

This tutorial demonstrates registering events defined as inline TypeScript interfaces, and published to Segment using their NodeJS and web browser SDKs. You can browse the `app` directory for [examples](./app/src/Component/HelpPopover.tsx#L19-L25) of events published using the web SDK, and the `server` directory for [examples](./server/cart.ts#L8-L12) published using their NodeJS SDK.

  *Note: This example project was originally based on [kopi-cloud/cabbage](https://github.com/kopi-cloud/cabbage)*
## Setup

From the `typescript` folder

1. Install the `gable` CLI

    You can install Gable's Python CLI using pip

    ```bash
    pip install gable --upgrade
    ```

    afterwards, confirm the version is at least `0.9.0`

    ```bash
    gable --version
      gable, version 0.9.0
    ```

2. Set your Gable API Key

    Log into Gable at `https://sandbox.<company>.gable.ai/`, and navigate to `Settings -> API Keys` from the side panel. Copy the API endpoint & API key values, and run the following in your terminal window

    ```bash
    export GABLE_API_ENDPOINT=<copied_api_endpoint>
    export GABLE_API_KEY=<copied_api_key>
    ```

## Register Segment Events

Once the setup is complete, you're ready to register the backend and frontend events defined in this project as data assets in Gable!

From the `typescript` folder run the below command to print out the list of events that will be registered as data assets in Gable. To register the events, remove the `--dry-run` flag.

```bash
gable data-asset register --source-type typescript --library segment --dry-run
```
