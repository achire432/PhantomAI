"""
MULTI-MODEL AI SERVICE
=======================
Purpose: Route requests to the appropriate AI model.

Why This Matters:
- One interface for all models
- Easy to switch between models
- Each model uses the same API

How It Works:
1. Check which model is active
2. Route the request to the correct model
3. Return the response

What Would Happen Without This:
- Each model would need separate code
- Switching models would be hard
- Code duplication
"""

import requests
import os
from typing import Optional, List, Dict, Any
from backend.app.models.ai_models import model_registry
from backend.app.services.ai import ask_ai as ask_local_ai

def ask_ai_with_model(prompt: str, context: Optional[List[Dict]] = None, model_name: Optional[str] = None) -> str:
    """
    Ask the AI using the specified model.
    
    Parameters:
    - prompt: The user's message
    - context: Previous messages for context
    - model_name: Optional specific model to use
    
    Returns:
    - The AI's response
    """
    
    # Use specified model or active model
    if model_name:
        active_model = model_registry.models.get(model_name)
    else:
        active_model = model_registry.get_active()
    
    if not active_model:
        return "Error: No active model found."
    
    # Route to the appropriate model
    if active_model.name == "qwen-4b":
        return ask_local_ai(prompt, context)
    
    elif active_model.provider == "Groq":
        return ask_groq(prompt, context, active_model.name)
    
    elif active_model.provider == "OpenAI":
        return ask_openai(prompt, context, active_model.name)
    
    elif active_model.provider == "Anthropic":
        return ask_anthropic(prompt, context, active_model.name)
    
    else:
        return f"Error: Model '{active_model.name}' not supported."

def ask_groq(prompt: str, context: Optional[List[Dict]] = None, model: str = "groq-llama3") -> str:
    """Send a request to Groq API."""
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Error: GROQ_API_KEY not set. Please add it to .env"
    
    # Map model names to Groq model IDs
    model_map = {
        "groq-llama3": "llama-3.1-8b-instant",
        "groq-mixtral": "mixtral-8x7b-32768"
    }
    
    model_id = model_map.get(model, "llama-3.1-8b-instant")
    
    # Build messages
    messages = []
    if context:
        for msg in context:
            messages.append(msg)
    messages.append({"role": "user", "content": prompt})
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model_id,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024
    }
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: {str(e)}"

def ask_openai(prompt: str, context: Optional[List[Dict]] = None, model: str = "gpt-4o") -> str:
    """Send a request to OpenAI API."""
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "Error: OPENAI_API_KEY not set. Please add it to .env"
    
    messages = []
    if context:
        for msg in context:
            messages.append(msg)
    messages.append({"role": "user", "content": prompt})
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024
    }
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: {str(e)}"

def ask_anthropic(prompt: str, context: Optional[List[Dict]] = None, model: str = "claude-3-opus") -> str:
    """Send a request to Anthropic Claude API."""
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return "Error: ANTHROPIC_API_KEY not set. Please add it to .env"
    
    # Build system prompt and messages
    system = "You are a helpful AI assistant called Phantom AI."
    messages = []
    
    if context:
        for msg in context:
            messages.append(msg)
    messages.append({"role": "user", "content": prompt})
    
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "system": system,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024
    }
    
    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        return response.json()["content"][0]["text"].strip()
    except Exception as e:
        return f"Error: {str(e)}"