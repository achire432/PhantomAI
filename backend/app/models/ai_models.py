"""
AI MODELS REGISTRY
===================
Purpose: Manage multiple AI models in PhantomAI.

Why This Matters:
- PhantomAI can use different models
- Switch between local and cloud models
- Each model has strengths
"""

from typing import Optional, List, Dict, Any
import os

class AIModel:
    """Represents an AI model."""
    
    def __init__(self, name: str, model_type: str, description: str, provider: str = "local"):
        self.name = name
        self.model_type = model_type
        self.description = description
        self.provider = provider
        self.is_active = False
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "type": self.model_type,
            "description": self.description,
            "provider": self.provider,
            "active": self.is_active
        }

class ModelRegistry:
    """Registry of all available AI models."""
    
    def __init__(self):
        self.models = {}
        self.active_model = None
    
    def register(self, model: AIModel):
        """Register a new model."""
        self.models[model.name] = model
    
    def activate(self, model_name: str) -> bool:
        """Activate a specific model."""
        if model_name in self.models:
            # Deactivate all models
            for m in self.models.values():
                m.is_active = False
            # Activate the selected model
            self.models[model_name].is_active = True
            self.active_model = model_name
            return True
        return False
    
    def get_active(self) -> Optional[AIModel]:
        """Get the currently active model."""
        if self.active_model:
            return self.models.get(self.active_model)
        return None
    
    def get_all(self) -> List[dict]:
        """Get all registered models."""
        return [m.to_dict() for m in self.models.values()]
    
    def get_model_names(self) -> List[str]:
        """Get all model names."""
        return list(self.models.keys())
    
    def get_available_models(self) -> List[dict]:
        """Get models that are available (API keys set)."""
        available = []
        for name, model in self.models.items():
            # Check if model is available
            if model.provider == "Local":
                available.append(model.to_dict())
            elif model.provider == "Groq" and os.getenv("GROQ_API_KEY"):
                available.append(model.to_dict())
            elif model.provider == "OpenAI" and os.getenv("OPENAI_API_KEY"):
                available.append(model.to_dict())
            elif model.provider == "Anthropic" and os.getenv("ANTHROPIC_API_KEY"):
                available.append(model.to_dict())
        return available

# Create the global registry
model_registry = ModelRegistry()

# Register all models
# 1. Local Model
model_registry.register(AIModel(
    name="qwen-4b",
    model_type="local",
    description="Qwen3-4B running locally. Free, private, but slow on Intel Mac.",
    provider="Local"
))

# 2. Groq Models (if API key is available)
if os.getenv("GROQ_API_KEY"):
    model_registry.register(AIModel(
        name="groq-llama3",
        model_type="cloud",
        description="Groq Llama 3.1 8B. Very fast, free tier available.",
        provider="Groq"
    ))
    
    model_registry.register(AIModel(
        name="groq-mixtral",
        model_type="cloud",
        description="Groq Mixtral 8x7B. Excellent reasoning, free tier available.",
        provider="Groq"
    ))

# 3. OpenAI Models (if API key is available)
if os.getenv("OPENAI_API_KEY"):
    model_registry.register(AIModel(
        name="gpt-4o",
        model_type="cloud",
        description="OpenAI GPT-4o. Powerful and versatile. Paid.",
        provider="OpenAI"
    ))
    
    model_registry.register(AIModel(
        name="gpt-4o-mini",
        model_type="cloud",
        description="OpenAI GPT-4o-mini. Fast and affordable. Paid.",
        provider="OpenAI"
    ))

# 4. Anthropic Models (if API key is available)
if os.getenv("ANTHROPIC_API_KEY"):
    model_registry.register(AIModel(
        name="claude-3-opus",
        model_type="cloud",
        description="Anthropic Claude 3 Opus. Thoughtful and detailed. Paid.",
        provider="Anthropic"
    ))

# Activate default model
model_registry.activate("qwen-4b")

def get_model_registry() -> ModelRegistry:
    """Get the model registry instance."""
    return model_registry