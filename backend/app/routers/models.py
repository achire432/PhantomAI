"""
MODEL ROUTER
=============
Purpose: Manage AI models in PhantomAI.

Endpoints:
- GET /models/ - List all available models
- GET /models/available - List only available models
- GET /models/active - Get the active model
- POST /models/activate/{name} - Activate a model
- GET /models/status - Get model status with explanations
"""

from fastapi import APIRouter, Depends, HTTPException
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.models.ai_models import model_registry
from backend.app.services.api_key_service import APIKeyManager

router = APIRouter(prefix="/models", tags=["Models"])

@router.get("/")
def list_models(current_user: User = Depends(get_current_user)):
    """
    List all registered AI models.
    """
    return {
        "models": model_registry.get_all(),
        "active": model_registry.active_model,
        "count": len(model_registry.models)
    }

@router.get("/available")
def get_available_models(current_user: User = Depends(get_current_user)):
    """
    List only models that are available (API keys set).
    """
    available = model_registry.get_available_models()
    return {
        "models": available,
        "active": model_registry.active_model,
        "count": len(available)
    }

@router.get("/active")
def get_active_model(current_user: User = Depends(get_current_user)):
    """
    Get the currently active model.
    """
    active = model_registry.get_active()
    if not active:
        return {"active": None, "message": "No active model"}
    return {
        "active": active.to_dict()
    }

@router.post("/activate/{model_name}")
def activate_model(
    model_name: str,
    current_user: User = Depends(get_current_user)
):
    """
    Activate a specific model.
    
    If the model requires an API key, it will check if the key is set.
    """
    # Check if model exists
    if model_name not in model_registry.models:
        raise HTTPException(status_code=404, detail=f"Model '{model_name}' not found")
    
    # Check if model is available
    model = model_registry.models[model_name]
    
    # Check API keys if needed
    if model.provider == "Groq" and not APIKeyManager.has_key("GROQ_API_KEY"):
        return {
            "error": "GROQ_API_KEY not set. Please add it to .env",
            "model": model_name,
            "available": False
        }
    elif model.provider == "OpenAI" and not APIKeyManager.has_key("OPENAI_API_KEY"):
        return {
            "error": "OPENAI_API_KEY not set. Please add it to .env",
            "model": model_name,
            "available": False
        }
    elif model.provider == "Anthropic" and not APIKeyManager.has_key("ANTHROPIC_API_KEY"):
        return {
            "error": "ANTHROPIC_API_KEY not set. Please add it to .env",
            "model": model_name,
            "available": False
        }
    
    # Activate the model
    model_registry.activate(model_name)
    
    return {
        "message": f"✅ Activated model: {model_name}",
        "model": model_registry.get_active().to_dict(),
        "provider": model.provider,
        "description": model.description
    }

@router.get("/status")
def get_model_status(current_user: User = Depends(get_current_user)):
    """
    Get detailed status of all models with explanations.
    """
    status = []
    for name, model in model_registry.models.items():
        is_available = False
        status_text = ""
        
        if model.provider == "Local":
            is_available = True
            status_text = "✅ Available (Running on your Mac)"
        elif model.provider == "Groq":
            is_available = APIKeyManager.has_key("GROQ_API_KEY")
            status_text = "✅ Available" if is_available else "❌ Needs GROQ_API_KEY in .env"
        elif model.provider == "OpenAI":
            is_available = APIKeyManager.has_key("OPENAI_API_KEY")
            status_text = "✅ Available" if is_available else "❌ Needs OPENAI_API_KEY in .env"
        elif model.provider == "Anthropic":
            is_available = APIKeyManager.has_key("ANTHROPIC_API_KEY")
            status_text = "✅ Available" if is_available else "❌ Needs ANTHROPIC_API_KEY in .env"
        
        status.append({
            "name": model.name,
            "provider": model.provider,
            "description": model.description,
            "available": is_available,
            "status": status_text,
            "active": model.is_active
        })
    
    return {
        "models": status,
        "active": model_registry.active_model
    }