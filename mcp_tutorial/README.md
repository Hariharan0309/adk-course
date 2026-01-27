# MCP Tutorial Project

This directory contains a tutorial project demonstrating how to build and integrate Agents using the **Agent Development Kit (ADK)** with the **[Model Context Protocol (MCP)](https://github.com/modelcontextprotocol/servers)**.

It showcases how to connect an ADK Agent to:
1.  A simple local MCP server (monitoring system stats).
2.  A complex, feature-rich MCP server (Google Workspace integration).

## Project Structure

```
mcp_tutorial/
├── adk_agent/              # The main Agent application built with ADK
│   ├── agent.py            # Agent definition and tool configuration
│   └── ...
├── local_mcp_server/       # A simple custom MCP server
│   ├── server.py           # Defines the 'get_system_stats' tool
│   └── ...
└── google_workspace_mcp/   # A comprehensive Google Workspace MCP server
    ├── main.py             # Entry point for the workspace server
    ├── README.md           # Documentation for the workspace server
    └── ...
```

## Components

### 1. ADK Agent (`adk_agent/`)

The core of this tutorial is the `adk_agent`. It is an LLM-powered agent configured to use tools provided by MCP servers.

*   **File:** `adk_agent/agent.py`
*   **Current Configuration:**
    *   **Name:** `System_Monitor_Agent`
    *   **Model:** `gemini-2.5-flash`
    *   **Tools:** Uses `MCPToolset` to connect to the `local_mcp_server` via stdio.
    *   **Capability:** Can answer questions about the local computer's health (CPU/RAM usage).

*   **Alternative Configuration (Commented Out):**
    *   The file also contains a commented-out configuration for a `Drive Assistant`.
    *   This configuration connects to the `google_workspace_mcp` server to interact with Google Drive (Search, Read, etc.).

### 2. Local MCP Server (`local_mcp_server/`)

A lightweight MCP server built using `mcp.server.fastmcp`.

*   **File:** `local_mcp_server/server.py`
*   **Tools Provided:**
    *   `get_system_stats`: Returns current CPU and Memory usage.
*   **Implementation:** Uses `psutil` to fetch system metrics.

### 3. Google Workspace MCP Server (`google_workspace_mcp/`)

A robust, feature-complete MCP server for Google Workspace.

*   **Purpose:** Provides tools to interact with Google Calendar, Drive, Gmail, Docs, Sheets, Slides, Forms, Tasks, and Chat.
*   **Integration:** Can be connected to the `adk_agent` to give it powers to manage your Google Workspace data.
*   See `google_workspace_mcp/README.md` for full details on this component.

## Getting Started

### Prerequisites

*   Python 3.10+
*   `uv` (recommended for dependency management) or `pip`

### Running the Agent

1.  **Navigate to the project directory:**
    ```bash
    cd mcp_tutorial
    ```

2.  **Ensure dependencies are installed** for the agent and the servers.

3.  **Run the Agent:**
    You can run the agent using the ADK CLI or by executing the script if configured.
    *(Note: Ensure the paths in `agent.py` point correctly to your local directories)*

### Switching Configs

To switch between the **System Monitor** and the **Google Drive Assistant**:
1.  Open `adk_agent/agent.py`.
2.  Comment out the currently active `root_agent` definition.
3.  Uncomment the desired `root_agent` definition.
4.  If using the Google Workspace agent, ensure you have updated the `env` variables (like `GOOGLE_CLIENT_SECRET_PATH` and `USER_GOOGLE_EMAIL`) with your actual credentials.
