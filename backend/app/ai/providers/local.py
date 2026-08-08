from typing import Optional, List, Dict

from backend.app.ai.providers.base import AIProvider


class LocalProvider(AIProvider):
    """
    Local AI provider.

    This currently connects to the existing
    Qwen3-4B implementation.
    """

    name = "Local"

    def generate(
        self,
        prompt: str,
        context: Optional[List[Dict]] = None,
        model: Optional[str] = None,
    ) -> str:

        from backend.app.services.ai import ask_ai

        return ask_ai(
            prompt=prompt,
            context=context,
        )