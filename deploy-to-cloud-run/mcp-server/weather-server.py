from mcp.server.fastmcp import FastMCP
import requests
import os

# Cloud Run injects the PORT environment variable automatically
port = int(os.environ.get("PORT", 8080))
# 1. Define the server
mcp = FastMCP("My Computer Agent", port=port, host="0.0.0.0")

@mcp.tool()
def get_weather(city: str) -> dict:
    """
    Fetches real-time weather data for a specific city.
    """
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    geo_response = requests.get(geo_url).json()
    
    if not geo_response.get("results"):
        return {"error": f"Could not find coordinates for {city}"}
        
    lat = geo_response["results"][0]["latitude"]
    lon = geo_response["results"][0]["longitude"]
    
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    weather_response = requests.get(weather_url).json()
    
    current = weather_response["current_weather"]
    
    return {
        "city": city,
        "temperature": f"{current['temperature']}°C",
        "condition_code": current["weathercode"]
    }

if __name__ == "__main__":
    # We use 'streamable-http' to ensure compatibility with Cloud Run's 
    # request-based scaling and lifecycle.
    mcp.run(transport="streamable-http")