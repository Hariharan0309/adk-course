from google.adk.agents.llm_agent import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types
import requests


def get_weather(city: str) -> dict:
    """
    Fetches real-time weather data for a specific city using the Open-Meteo API.
    Args:
        city: The name of the city (e.g., "London", "Berlin", "Tokyo").
    """
    print(f"\n[TOOL CALL] 🌍 Connecting to public weather satellite for: {city}...")
    
    # Step A: We need coordinates first (Geocoding)
    # Using Open-Meteo's free geocoding API (No Key Required)
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    geo_response = requests.get(geo_url).json()
    
    if not geo_response.get("results"):
        return {"error": f"Could not find coordinates for {city}"}
        
    lat = geo_response["results"][0]["latitude"]
    lon = geo_response["results"][0]["longitude"]
    
    # Step B: Get the actual weather
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    weather_response = requests.get(weather_url).json()
    
    current = weather_response["current_weather"]
    
    return {
        "city": city,
        "temperature": f"{current['temperature']}°C",
        "windspeed": f"{current['windspeed']} km/h",
        "condition_code": current["weathercode"]
    }

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)


root_agent = Agent(
    model=Gemini(model="gemini-2.5-flash", retry_options=retry_config),
    name="weather_bot",
    instruction="You are a helpful weather assistant. Always use the get_weather tool to answer questions.",
    tools=[get_weather]
)
