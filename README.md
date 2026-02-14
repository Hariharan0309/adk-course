# ADK Course Projects

This repository contains examples and projects built using the **Google Agent Development Kit (ADK)**.

## Available Agents

### 1. `myAgent`
A basic conversational agent initialized with the `gemini-2.5-flash` model. It serves as a simple starting point for understanding ADK agent structure.

### 2. `weather_agent`
A functional weather assistant capable of fetching real-time weather data.
- **Model:** `gemini-2.5-flash`
- **Tools:** `get_weather` (uses Open-Meteo API)
- **Features:** Demonstrates tool usage and custom retry configurations for API calls.

### 3. `newsletter_agent`
An automated editorial team that researches, drafts, and edits a weekly developer newsletter.
- **Model:** `gemini-2.5-flash-lite`
- **Tools:** `google_search`, `exit_loop`
- **Features:** Showcases complex architectures:
    - **ParallelAgent:** Runs `ai_news_agent` and `hackathon_agent` simultaneously.
    - **LoopAgent:** Cycles between a `newsletter_writer` and `editor_agent` for quality control.

### 4. `remainder_agent`
A task management agent that helps users track reminders.
- **Model:** Gemini (via ADK)
- **Tools:** `add_remainder`, `remove_remainder`
- **Features:**
    - Interactive CLI chat.
    - Persistent SQLite storage (`my_agent_data.db`).

### 5. `memory` (Memory Agent)
An agent demonstrating long-term memory capabilities using Vertex AI Memory Bank.
- **Model:** `gemini-2.5-flash`
- **Features:**
    - Persists conversation history to Vertex AI.
    - Proactively searches memory for context.
    - Demonstrates `PreloadMemoryTool` and auto-save callbacks.

## Tutorials

### `mcp_tutorial`
A comprehensive guide on integrating the **Model Context Protocol (MCP)** with ADK agents.
- **Includes:**
    - `adk_agent`: The core agent connecting to MCP servers.
    - `local_mcp_server`: A simple server monitoring system stats (CPU/RAM).
    - `google_workspace_mcp`: A complex server for Google Workspace integration (Drive, Docs, Gmail, etc.).

## Deployment Guides

### `deploy-to-cloud-run`
Instructions and configuration for deploying ADK agents to **Google Cloud Run** as scalable web services.

### `deploy-to-vertexai`
Guide for deploying agents to **Vertex AI Agent Engine**, allowing for managed reasoning engines and remote execution.

## Getting Started

To run any of the agents in this repository, navigate to the project root (`adk-course`) and use the ADK CLI.

```bash
adk web
```
