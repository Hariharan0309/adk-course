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


## Getting Started

To run any of the agents in this repository, navigate to the project root (`adk-course`) and use the ADK CLI.

```bash
adk web
```