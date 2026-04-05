"""
Weather Agent — Remote A2A Agent (Google ADK)
=============================================
This agent is exposed via the A2A protocol so other agents
(including agents from different frameworks) can call it remotely.

Start server:
    adk api_server --a2a --port 8001 a2a/weather_agent

Agent card will be at:
    http://localhost:8001/a2a/weather_agent/.well-known/agent.json
"""

import requests
from google.adk.agents import Agent


def get_weather(city: str) -> dict:
    """
    Fetches real-time weather data for any city using the free Open-Meteo API.
    No API key required!

    Args:
        city: Name of the city (e.g., "Tokyo", "Paris", "New York")
    Returns:
        dict with temperature, windspeed, and condition code
    """
    # Step 1: Geocoding — get lat/lon for the city
    geo_url = (
        f"https://geocoding-api.open-meteo.com/v1/search"
        f"?name={city}&count=1&language=en&format=json"
    )
    geo_response = requests.get(geo_url, timeout=10).json()

    if not geo_response.get("results"):
        return {"error": f"Could not find location for city: {city}"}

    lat = geo_response["results"][0]["latitude"]
    lon = geo_response["results"][0]["longitude"]

    # Step 2: Get actual weather data
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )
    weather_data = requests.get(weather_url, timeout=10).json()
    current = weather_data["current_weather"]

    # Map weather codes to human-readable conditions
    weather_codes = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Foggy", 48: "Icy fog", 51: "Light drizzle", 61: "Slight rain",
        71: "Slight snow", 80: "Slight rain showers", 95: "Thunderstorm",
    }
    condition = weather_codes.get(current["weathercode"], f"Code {current['weathercode']}")

    return {
        "city": city,
        "temperature": f"{current['temperature']}°C",
        "windspeed": f"{current['windspeed']} km/h",
        "condition": condition,
        "is_day": bool(current.get("is_day", 1)),
    }


# ─── ADK Agent Definition ─────────────────────────────────────────────────────
# This `root_agent` variable is what ADK looks for when serving via A2A
root_agent = Agent(
    model="gemini-2.0-flash",
    name="weather_agent",
    instruction=(
        "You are a friendly weather expert. "
        "When asked about weather in any city, always use the get_weather tool. "
        "Report the temperature, wind speed, and sky condition in a natural, "
        "conversational way. If the user asks about multiple cities, call the tool for each one."
    ),
    tools=[get_weather],
)
