# Weather MCP Server Deployment

This guide describes how to deploy the Weather MCP Server to Google Cloud Run.

## Prerequisites

- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed and configured.
- A Google Cloud Project set up.

## Deployment Steps

Run the following commands to build the container image and deploy it to Cloud Run.

### 1. Build and Submit the Image

Build the Docker image and submit it to the Google Container Registry (GCR):

```bash
gcloud builds submit --tag gcr.io/$(gcloud config get-value project)/weather-mcp-server
```

### 2. Deploy to Cloud Run

Deploy the image to Cloud Run as a managed service, allowing unauthenticated access:

```bash
gcloud run deploy weather-mcp-server --image gcr.io/$(gcloud config get-value project)/weather-mcp-server --platform managed --allow-unauthenticated
```
