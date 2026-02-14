# Deploy to Vertex AI (Agent Engine)

This directory contains instructions for deploying your ADK Agent to Google Cloud Vertex AI Agent Engine.

## Prerequisites

1.  **Google Cloud Project**: You need a Google Cloud project.
2.  **Billing Enabled**: Ensure billing is enabled for your project.
3.  **gcloud CLI**: Install the [Google Cloud CLI](https://cloud.google.com/sdk/docs/install).

## Configuration & Deployment Steps

Follow these exact steps to authenticate and deploy your agent.

### 1. Enable Required APIs

Go to the Google Cloud Console and enable the following APIs for your project:
*   **Vertex AI API**
*   **Cloud Resource Manager API**

### 2. Authenticate Your Environment

Run the following commands in your terminal to authenticate with Google Cloud.

**Login to gcloud:**
```bash
gcloud auth login
```

**Set your project:**
Replace `MY-PROJECT-ID` with your actual project ID.
```bash
gcloud config set project MY-PROJECT-ID
```

**Authenticate Application Default Credentials (ADC):**
This allows your local code (and the ADK CLI) to use your user credentials.
```bash
gcloud auth application-default login
```

### 3. Deploy the Agent

Use the `adk` CLI to deploy your agent to the Agent Engine.

**Command Syntax:**
```bash
PROJECT_ID=your-project-id
LOCATION_ID=us-central1  # e.g., us-central1, europe-west4, etc.
DISPLAY_NAME="Weather Agent" # The name you want to see in the console
AGENT_DIR=weather_agent # The directory containing your agent code

adk deploy agent_engine \
  --project=$PROJECT_ID \
  --region=$LOCATION_ID \
  --display_name="$DISPLAY_NAME" \
  $AGENT_DIR
```

**Example:**
```bash
adk deploy agent_engine \
  --project=valued-mediator-461216-k7 \
  --region=us-central1 \
  --display_name="Weather Bot" \
  weather_agent
```

## Testing the Deployed Agent

### 1. Using Python (`remote_session.py`)

After deployment, you can use the `remote_session.py` script to interact with your agent.

1.  Open `remote_session.py`.
2.  Update the `RESOURCE_ID` with the resource name outputted by the deployment command (e.g., `projects/.../locations/.../reasoningEngines/...`).
3.  Run the script:
    ```bash
    python remote_session.py
    ```

### 2. Using cURL

You can also verify the deployment and interact with the agent using `curl`.

**1. Setup Variables**
```bash
PROJECT_ID="valued-mediator-461216-k7"
LOCATION_ID="us-central1"
# Replace with your actual Reasoning Engine ID (e.g., 1234567890)
REASONING_ENGINE_ID="7301622524083699712" 
```

**2. List Reasoning Engines**
Use this to find your `REASONING_ENGINE_ID` if you don't have it.
```bash
curl -X GET \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
"https://${LOCATION_ID}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION_ID}/reasoningEngines"
```

**3. Create a Session**
The ADK agent manages sessions via the `create_session` method.
```bash
curl -X POST \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
"https://${LOCATION_ID}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION_ID}/reasoningEngines/${REASONING_ENGINE_ID}:query" \
-d '{
  "classMethod": "async_create_session",
  "input": {
    "user_id": "curl-test-user"
  }
}'
```
*Copy the `name` (Session ID) from the response JSON.*

**4. Stream a Query**
Replace `YOUR_SESSION_ID` with the ID from the previous step.
```bash
SESSION_ID="3705760042834722816"

curl -X POST \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
"https://${LOCATION_ID}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION_ID}/reasoningEngines/${REASONING_ENGINE_ID}:streamQuery" \
-d '{
  "classMethod": "stream_query",
  "input": {
    "user_id": "curl-test-user",
    "session_id": "'"${SESSION_ID}"'",
    "message": "What is the weather in Chennai right now?"
  }
}'
```
