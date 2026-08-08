from abc import ABC, abstractmethod
from typing import Optional, List, Dict


class AIProvider(ABC):
    """
    Base interface for every PhantomAI AI provider.

    Every future provider such as:
        - Groq
        - OpenAI
        - Anthropic
        - Gemini
        - Local Qwen
        - etc.

    should follow this interface.
    """

    name = "base"

    @abstractmethod
    def generate(
        self,
        prompt: str,
        context: Optional[List[Dict]] = None,
        model: Optional[str] = None,
    ) -> str:
        """
        Generate an AI response.
        """
        raise NotImplementedError