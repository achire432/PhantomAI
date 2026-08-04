"""
WEATHER ROUTER
===============
Purpose: Handle weather API requests.

Endpoint:
- GET /weather/{city} - Get weather for a city

Why We Need This:
- Users can ask about weather
- Only authenticated users can access
- Returns formatted weather data
"""

from fastapi import APIRouter, Depends, HTTPException
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.services.weather_service import get_weather

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/{city}")
def weather(
    city: str,
    current_user: User = Depends(get_current_user)
):
    """Get current weather for a city."""
    result = get_weather(city)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Failed to get weather"))
    return result