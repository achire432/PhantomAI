"""
API KEY SERVICE
================
Purpose: Manage API keys securely.

Why This Matters:
- API keys are sensitive information
- Must be stored in .env, not in code
- Need to check if keys are available
- Must handle missing keys gracefully
"""

import os
from typing import Dict, Any

class APIKeyManager:
    """Manage API keys for various services."""
    
    # Define all required API keys and their status
    KEYS = {
        "GROQ_API_KEY": {
            "service": "Groq",
            "url": "https://console.groq.com",
            "description": "Free tier available. For fast AI responses.",
            "required": False
        },
        "OPENAI_API_KEY": {
            "service": "OpenAI",
            "url": "https://platform.openai.com",
            "description": "Paid. For GPT-4 and DALL-E.",
            "required": False
        },
        "ANTHROPIC_API_KEY": {
            "service": "Anthropic Claude",
            "url": "https://console.anthropic.com",
            "description": "Paid. For Claude models.",
            "required": False
        },
        "STABILITY_API_KEY": {
            "service": "Stability AI",
            "url": "https://platform.stability.ai",
            "description": "Free tier available. For image generation.",
            "required": False
        },
        "OPENWEATHER_API_KEY": {
            "service": "OpenWeather",
            "url": "https://openweathermap.org",
            "description": "Free tier available. For weather data.",
            "required": False
        }
    }
    
    @classmethod
    def get_key(cls, key_name: str) -> str:
        """Get an API key from environment."""
        return os.getenv(key_name, "")
    
    @classmethod
    def has_key(cls, key_name: str) -> bool:
        """Check if an API key is set."""
        key = cls.get_key(key_name)
        return bool(key) and key != f"your_{key_name.lower()}_here"
    
    @classmethod
    def get_status(cls, key_name: str) -> Dict[str, Any]:
        """Get detailed status of an API key."""
        info = cls.KEYS.get(key_name, {})
        is_set = cls.has_key(key_name)
        
        return {
            "name": key_name,
            "service": info.get("service", "Unknown"),
            "url": info.get("url", ""),
            "description": info.get("description", ""),
            "is_set": is_set,
            "status": "✅ Available" if is_set else "❌ Not Set",
            "required": info.get("required", False)
        }
    
    @classmethod
    def get_all_status(cls) -> Dict[str, Any]:
        """Get status of all API keys."""
        status = {}
        for key_name in cls.KEYS:
            status[key_name] = cls.get_status(key_name)
        return status
    
    @classmethod
    def get_available_services(cls) -> list:
        """Get list of services with API keys set."""
        available = []
        for key_name, info in cls.KEYS.items():
            if cls.has_key(key_name):
                available.append(info["service"])
        return available
    
    @classmethod
    def get_missing_keys(cls) -> list:
        """Get list of missing API keys."""
        missing = []
        for key_name, info in cls.KEYS.items():
            if not cls.has_key(key_name):
                missing.append(key_name)
        return missing