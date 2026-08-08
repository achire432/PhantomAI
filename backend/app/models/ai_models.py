import os
from typing import List, Optional


class AIModel:
    """
    Represents an AI model registered inside PhantomAI.

    This class only describes the model.
    It does not communicate with the provider.
    """

    def __init__(
        self,
        name: str,
        model_type: str,
        description: str,
        provider: str,
        provider_model: Optional[str] = None,
        requires_api_key: bool = False,
    ):
        self.name = name
        self.model_type = model_type
        self.description = description
        self.provider = provider
        self.provider_model = provider_model or name
        self.requires_api_key = requires_api_key
        self.is_active = False

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "type": self.model_type,
            "description": self.description,
            "provider": self.provider,
            "provider_model": self.provider_model,
            "requires_api_key": self.requires_api_key,
            "active": self.is_active,
        }


class ModelRegistry:
    """
    Central registry for all PhantomAI AI models.

    The registry knows:
    - which models exist
    - which provider they belong to
    - which model is active
    - whether a model is available
    """

    def __init__(self):
        self.models = {}
        self.active_model: Optional[str] = None

    # ========================================================
    # REGISTER
    # ========================================================

    def register(self, model: AIModel) -> None:
        """Register an AI model."""
        self.models[model.name] = model

    # ========================================================
    # ACTIVATE
    # ========================================================

    def activate(self, model_name: str) -> bool:
        """
        Activate one model and deactivate all others.
        """

        if model_name not in self.models:
            return False

        selected_model = self.models[model_name]

        if not self.is_available(model_name):
            return False

        for model in self.models.values():
            model.is_active = False

        selected_model.is_active = True
        self.active_model = model_name

        return True

    # ========================================================
    # GET ACTIVE
    # ========================================================

    def get_active(self) -> Optional[AIModel]:
        """Return the currently active model."""

        if self.active_model is None:
            return None

        return self.models.get(self.active_model)

    # ========================================================
    # GET MODEL
    # ========================================================

    def get(self, model_name: str) -> Optional[AIModel]:
        """Return one registered model."""

        return self.models.get(model_name)

    # ========================================================
    # GET ALL
    # ========================================================

    def get_all(self) -> List[dict]:
        """Return all registered models."""

        return [
            model.to_dict()
            for model in self.models.values()
        ]

    # ========================================================
    # MODEL NAMES
    # ========================================================

    def get_model_names(self) -> List[str]:
        """Return all registered model names."""

        return list(self.models.keys())

    # ========================================================
    # AVAILABILITY
    # ========================================================

    def is_available(self, model_name: str) -> bool:
        """
        Check whether a model can currently be used.
        """

        model = self.models.get(model_name)

        if not model:
            return False

        if not model.requires_api_key:
            return True

        if model.provider == "Groq":
            return bool(os.getenv("GROQ_API_KEY"))

        if model.provider == "OpenAI":
            return bool(os.getenv("OPENAI_API_KEY"))

        if model.provider == "Anthropic":
            return bool(os.getenv("ANTHROPIC_API_KEY"))

        if model.provider == "Google":
            return bool(os.getenv("GOOGLE_API_KEY"))

        if model.provider == "DeepSeek":
            return bool(os.getenv("DEEPSEEK_API_KEY"))

        return False

    # ========================================================
    # AVAILABLE MODELS
    # ========================================================

    def get_available_models(self) -> List[dict]:
        """
        Return models that are currently available.
        """

        available = []

        for model in self.models.values():

            if self.is_available(model.name):
                available.append(model.to_dict())

        return available


# ============================================================
# GLOBAL MODEL REGISTRY
# ============================================================

model_registry = ModelRegistry()


# ============================================================
# LOCAL MODEL
# ============================================================

model_registry.register(
    AIModel(
        name="qwen-4b",
        model_type="local",
        description="Qwen3-4B running locally on this computer.",
        provider="Local",
        provider_model="qwen-4b",
        requires_api_key=False,
    )
)


# ============================================================
# GROQ
# ============================================================

if os.getenv("GROQ_API_KEY"):

    model_registry.register(
        AIModel(
            name="groq-llama3",
            model_type="cloud",
            description="Llama 3.1 8B running through Groq.",
            provider="Groq",
            provider_model="llama-3.1-8b-instant",
            requires_api_key=True,
        )
    )


# ============================================================
# OPENAI
# ============================================================

if os.getenv("OPENAI_API_KEY"):

    model_registry.register(
        AIModel(
            name="gpt-4o-mini",
            model_type="cloud",
            description="OpenAI GPT-4o-mini.",
            provider="OpenAI",
            provider_model="gpt-4o-mini",
            requires_api_key=True,
        )
    )


# ============================================================
# ANTHROPIC
# ============================================================

if os.getenv("ANTHROPIC_API_KEY"):

    model_registry.register(
        AIModel(
            name="claude-3-opus",
            model_type="cloud",
            description="Anthropic Claude.",
            provider="Anthropic",
            provider_model="claude-3-opus",
            requires_api_key=True,
        )
    )


# ============================================================
# GOOGLE
# ============================================================

if os.getenv("GOOGLE_API_KEY"):

    model_registry.register(
        AIModel(
            name="gemini",
            model_type="cloud",
            description="Google Gemini model.",
            provider="Google",
            provider_model="gemini",
            requires_api_key=True,
        )
    )


# ============================================================
# DEEPSEEK
# ============================================================

if os.getenv("DEEPSEEK_API_KEY"):

    model_registry.register(
        AIModel(
            name="deepseek",
            model_type="cloud",
            description="DeepSeek AI model.",
            provider="DeepSeek",
            provider_model="deepseek-chat",
            requires_api_key=True,
        )
    )


# ============================================================
# DEFAULT MODEL
# ============================================================

if "groq-llama3" in model_registry.models:

    model_registry.activate("groq-llama3")

elif "qwen-4b" in model_registry.models:

    model_registry.activate("qwen-4b")


# ============================================================
# HELPER
# ============================================================

def get_model_registry() -> ModelRegistry:
    """Return the global model registry."""

    return model_registry