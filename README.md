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

## Getting Started

To run any of the agents in this repository, navigate to the project root (`adk-course`) and use the ADK CLI.

```bash
adk web
```