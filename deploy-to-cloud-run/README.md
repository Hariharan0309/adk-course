# Agent Deployment to Google Cloud Run

This guide outlines the steps to deploy your ADK agent to Google Cloud Run.

## Prerequisites

- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed and configured.
- `adk` (Agent Development Kit) installed.
- A valid Google Cloud Project.

## Deployment Steps

Run the following commands in your terminal to configure the environment and deploy the agent.

### 1. Set Environment Variables

Configure the deployment parameters by exporting the following variables.

> **Note:** Update `AGENT_PATH` to point to your specific agent directory (e.g., `./myAgent`).

```bash
# Set your Google Cloud Project ID
export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"

# Set your desired Google Cloud Location
export GOOGLE_CLOUD_LOCATION="us-central1" # Example: us-central1

# Set the path to your agent code directory
# Ensure this points to the folder containing your agent.py
export AGENT_PATH="./myAgent" 

# Set a name for your Cloud Run service (optional)
export SERVICE_NAME="my-agent-service"

# Set an application name (optional)
export APP_NAME="MyAgentApp"
```

### 2. Deploy the Agent

Use the `adk deploy` command to deploy your agent to Cloud Run. The `--with_ui` flag enables the adk web UI.

```bash
adk deploy cloud_run \
  --project=$GOOGLE_CLOUD_PROJECT \
  --region=$GOOGLE_CLOUD_LOCATION \
  --service_name=$SERVICE_NAME \
  --app_name=$APP_NAME \
  --with_ui \
  $AGENT_PATH
```

```