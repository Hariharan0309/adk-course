# Memory Agent

This agent demonstrates how to integrate **Vertex AI Memory Bank Service** with the Google ADK (Agent Development Kit). It showcases the ability to persist conversation history and retrieve relevant context using Google's Agent Engine.

## Features

- **Persistent Memory**: Automatically saves session interactions to a Vertex AI Memory Bank.
- **Context Retrieval**: Proactively searches memory for relevant information before answering (demonstrated in the startup logic).
- **Interactive CLI**: Provides a command-line interface to chat with the agent.
- **Agent Engine Integration**: Automatically creates or connects to an existing Agent Engine on Vertex AI.

## Prerequisites

Ensure you have the following environment variables set in a `.env` file in the root directory:

```env
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_API_KEY=your_gemini_api_key
AGENT_ENGINE_ID=optional_existing_engine_id
```

- If `AGENT_ENGINE_ID` is not provided, the script will create a new Agent Engine and print the ID. You should save this ID to your `.env` file to reuse the same memory bank in future runs.

## Structure

- **`agent.py`**: The main entry point. It sets up the `VertexAiMemoryBankService`, configures the `Agent` with `PreloadMemoryTool` and an auto-save callback, and starts the interactive session.
- **`utils.py`**: Helper functions for handling the interactive CLI session loop.

## Usage

1.  **Install Dependencies**: Ensure you have the required packages installed (typically via `pip install -r requirements.txt` in the project root, assuming the ADK and other libs are listed).
2.  **Run the Agent**:

    ```bash
    python memory/agent.py
    ```

3.  **Interact**: Type your messages in the console. Type `exit` or `quit` to end the session.

## How it Works

1.  **Initialization**: The script connects to Vertex AI. If no Agent Engine ID is found, it provisions a new one configured with `gemini-2.5-flash`.
2.  **Memory Hook**: The `auto_save_session_to_memory_callback` function is registered as an `after_agent_callback`. This ensures that after every interaction, the conversation turn is stored in the memory bank.
3.  **Preload**: The agent uses `PreloadMemoryTool` to potentially load context.
4.  **Search**: On startup, the script performs a test search ("What is my friend name ?") to demonstrate programmatic memory access.
