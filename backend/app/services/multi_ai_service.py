from typing import Optional, List, Dict

from backend.app.models.ai_models import model_registry

from backend.app.ai.providers.base import AIProvider
from backend.app.ai.providers.groq import GroqProvider
from backend.app.ai.providers.local import LocalProvider


# ============================================================
# PROVIDER REGISTRY
# ============================================================

PROVIDERS = {
    "Groq": GroqProvider(),
    "Local": LocalProvider(),
}


# ============================================================
# GET PROVIDER
# ============================================================

def get_provider(
    provider_name: str,
) -> Optional[AIProvider]:

    return PROVIDERS.get(
        provider_name
    )


# ============================================================
# MAIN AI ROUTER
# ============================================================

def ask_ai_with_model(
    prompt: str,
    context: Optional[List[Dict]] = None,
    model_name: Optional[str] = None,
) -> str:
    """
    Main PhantomAI AI router.

    The rest of PhantomAI should call this function.

    It decides:
        1. Which model is selected.
        2. Which provider owns that model.
        3. Which provider adapter handles the request.
    """

    # --------------------------------------------------------
    # SELECT MODEL
    # --------------------------------------------------------

    if model_name:

        active_model = model_registry.models.get(
            model_name
        )

    else:

        active_model = model_registry.get_active()

    # --------------------------------------------------------
    # NO MODEL
    # --------------------------------------------------------

    if not active_model:

        return (
            "No active AI model is configured."
        )

    # --------------------------------------------------------
    # SELECT PROVIDER
    # --------------------------------------------------------

    provider = get_provider(
        active_model.provider
    )

    if not provider:

        return (
            f"AI provider "
            f"'{active_model.provider}' "
            f"is not supported."
        )

    # --------------------------------------------------------
    # GENERATE RESPONSE
    # --------------------------------------------------------

    return provider.generate(
        prompt=prompt,
        context=context,
        model=active_model.name,
    )


# ============================================================
# PROVIDER INFORMATION
# ============================================================

def get_available_providers() -> List[str]:
    """
    Return providers currently implemented
    inside PhantomAI.
    """

    return list(
        PROVIDERS.keys()
    )


# ============================================================
# MODEL INFORMATION
# ============================================================

def get_available_models() -> List[dict]:
    """
    Return models that are currently available.
    """

    return model_registry.get_available_models()

# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def ask_groq(
    prompt: str,
    context: Optional[List[Dict]] = None,
    model: str = "groq-llama3",
) -> str:
    """
    Backward-compatible Groq function.

    Older PhantomAI services may still import ask_groq()
    directly.
    """

    provider = get_provider("Groq")

    if provider is None:
        return "Groq provider is not configured."

    return provider.generate(
        prompt=prompt,
        context=context,
        model=model,
    )