import os
from typing import List, Optional


class AIModel:
    """Represents an AI model."""

    def __init__(
        self,
        name: str,
        model_type: str,
        description: str,
        provider: str = "Local",
    ):
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
            "active": self.is_active,
        }


class ModelRegistry:
    """Registry of available AI models."""

    def __init__(self):
        self.models = {}
        self.active_model: Optional[str] = None

    def register(self, model: AIModel) -> None:
        """Register an AI model."""
        self.models[model.name] = model

    def activate(self, model_name: str) -> bool:
        """Activate one model and deactivate all others."""

        if model_name not in self.models:
            return False

        for model in self.models.values():
            model.is_active = False

        selected_model = self.models[model_name]
        selected_model.is_active = True
        self.active_model = model_name

        return True

    def get_active(self) -> Optional[AIModel]:
        """Return the currently active model."""

        if self.active_model is None:
            return None

        return self.models.get(self.active_model)

    def get_all(self) -> List[dict]:
        """Return all registered models."""
        return [
            model.to_dict()
            for model in self.models.values()
        ]

    def get_model_names(self) -> List[str]:
        """Return all model names."""
        return list(self.models.keys())

    def get_available_models(self) -> List[dict]:
        """Return models whose required API keys are available."""

        available = []

        for model in self.models.values():
            if model.provider == "Local":
                available.append(model.to_dict())

            elif (
                model.provider == "Groq"
                and os.getenv("GROQ_API_KEY")
            ):
                available.append(model.to_dict())

            elif (
                model.provider == "OpenAI"
                and os.getenv("OPENAI_API_KEY")
            ):
                available.append(model.to_dict())

            elif (
                model.provider == "Anthropic"
                and os.getenv("ANTHROPIC_API_KEY")
            ):
                available.append(model.to_dict())

        return available


model_registry = ModelRegistry()


# ---------------------------------------------------------
# LOCAL MODEL
# ---------------------------------------------------------

model_registry.register(
    AIModel(
        name="qwen-4b",
        model_type="local",
        description=(
            "Qwen3-4B running locally."
        ),
        provider="Local",
    )
)


# ---------------------------------------------------------
# GROQ MODELS
# ---------------------------------------------------------

if os.getenv("GROQ_API_KEY"):
    model_registry.register(
        AIModel(
            name="groq-llama3",
            model_type="cloud",
            description=(
                "Llama 3.1 8B running through Groq."
            ),
            provider="Groq",
        )
    )


# ---------------------------------------------------------
# OPENAI MODELS
# ---------------------------------------------------------

if os.getenv("OPENAI_API_KEY"):
    model_registry.register(
        AIModel(
            name="gpt-4o-mini",
            model_type="cloud",
            description="OpenAI GPT-4o-mini.",
            provider="OpenAI",
        )
    )


# ---------------------------------------------------------
# ANTHROPIC MODELS
# ---------------------------------------------------------

if os.getenv("ANTHROPIC_API_KEY"):
    model_registry.register(
        AIModel(
            name="claude-3-opus",
            model_type="cloud",
            description="Anthropic Claude.",
            provider="Anthropic",
        )
    )


# ---------------------------------------------------------
# DEFAULT MODEL
# ---------------------------------------------------------

if "groq-llama3" in model_registry.models:
    model_registry.activate("groq-llama3")
else:
    model_registry.activate("qwen-4b")


def get_model_registry() -> ModelRegistry:
    """Return the global model registry."""
    return model_registry