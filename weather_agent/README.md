# Weather Agent

A weather assistant built with the Google Agent Development Kit (ADK) that can look up real-time weather information.

## Description

This agent utilizes the `gemini-2.5-flash` model and is equipped with a custom tool (`get_weather`) to fetch weather data.

### Features
- **Real-time Data:** Uses the Open-Meteo API (no API key required) to get weather forecasts.
- **Tool Use:** Demonstrates how to define and register python functions as tools for the agent.
- **Robustness:** Includes custom HTTP retry options for model inference.

## How to Run

Ensure you have the Google ADK installed and configured.

1. Navigate to the project root directory (`adk-course`).

2. Run the agent using the ADK web interface:
   ```bash
   adk web
   ```
