"""
WEATHER SERVICE
================
Purpose: Get current weather information.

Why We Need This:
- Users ask about weather daily
- Free and simple to implement

How It Works:
- Uses OpenWeatherMap API
- API key is read from .env (never hardcoded!)
- Returns temperature, condition, humidity, wind

What You Need:
1. Sign up at https://openweathermap.org/api
2. Get your FREE API key
3. Add to .env: OPENWEATHER_API_KEY=your_key_here
"""

import requests
import os

# Read API key from environment - NEVER hardcode!
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city: str) -> dict:
    """
    Get current weather for a city.
    
    Example:
        get_weather("Kampala")
        → {"city": "Kampala", "temperature": 27, "condition": "Sunny", ...}
    """
    # Check if API key is set
    if not OPENWEATHER_API_KEY:
        return {
            "success": False,
            "error": "Weather API key not set. Please add OPENWEATHER_API_KEY to .env file."
        }
    
    try:
        params = {
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"  # Celsius
        }
        
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        return {
            "success": True,
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "condition": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
        
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            return {"success": False, "error": "Invalid API key. Please check your OPENWEATHER_API_KEY"}
        elif response.status_code == 404:
            return {"success": False, "error": f"City '{city}' not found"}
        else:
            return {"success": False, "error": f"HTTP error: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}