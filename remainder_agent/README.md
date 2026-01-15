# Remainder Agent

This agent helps users manage and track their remainders effectively using the Google Agent Development Kit (ADK) and the Gemini model.

## Features

- **Manage Remainders:** Add and remove remainders from your list.
- **Interactive CLI:** Chat with the agent directly in your terminal.
- **Persistent Storage:** Uses a local SQLite database (`my_agent_data.db`) to save your session and remainders.
- **Tools:** Equipped with custom tools (`add_remainder`, `remove_remainder`) to programmatically update your list.

## Prerequisites

- Python 3.x
- A Google Cloud Project with the Gemini API enabled.
- An API Key for the Gemini API.

## Setup

1.  **Environment Variables:**
    Ensure you have a `.env` file in the root of your project (or accessible to the script) containing your Google API Key:

    ```bash
    GOOGLE_API_KEY=your_api_key_here
    ```

2.  **Dependencies:**
    Make sure you have installed the necessary packages as per the project's `requirements.txt` (or ensure `google-adk`, `python-dotenv`, `google-genai` are installed).

## Usage

To start the agent, run the `agent.py` script from the project root or the agent directory:

```bash
python remainder_agent/agent.py
```

Or if you are inside the `remainder_agent` directory:

```bash
python agent.py
```

## Interaction

Once the agent is running, you can type natural language commands such as:
- "Remind me to buy milk."
- "What are my remainders?"
- "Remove the remainder about buying milk."
- "exit" or "quit" to stop the session.

## File Structure

- `agent.py`: The main entry point, configuring the agent, model, and session runner.
- `utils.py`: Contains the interactive session logic and the tool implementations (`add_remainder`, `remove_remainder`).
- `my_agent_data.db`: Auto-generated SQLite database file for session persistence.
