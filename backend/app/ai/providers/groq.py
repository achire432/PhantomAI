import os
from typing import Optional, List, Dict

import requests

from backend.app.ai.providers.base import AIProvider


GROQ_API_URL = (
    "https://api.groq.com/openai/v1/chat/completions"
)


class GroqProvider(AIProvider):
    """
    Groq AI provider.

    Handles all Groq models through the same provider.
    """

    name = "Groq"

    MODEL_MAP = {
        "groq-llama3": "llama-3.1-8b-instant",
        "groq-mixtral": "mixtral-8x7b-32768",
    }

    def generate(
        self,
        prompt: str,
        context: Optional[List[Dict]] = None,
        model: Optional[str] = None,
    ) -> str:

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            return "GROQ_API_KEY is not configured."

        model_name = model or "groq-llama3"

        model_id = self.MODEL_MAP.get(
            model_name,
            model_name,
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "CORE RULES:\n"
                    "- Answer the user's question directly.\n"
                    "- Use supplied long-term memory when relevant.\n"
                    "- Long-term memory represents the user's "
                    "current known preferences, goals, projects, "
                    "and facts.\n"
                    "- If conversation history conflicts with "
                    "long-term memory, prefer long-term memory.\n"
                    "- If the latest user message updates an old "
                    "fact, treat the latest value as current.\n"
                    "- Never invent personal information.\n"
                    "- Do not expose internal memory mechanisms "
                    "unless the user explicitly asks.\n"
                    "- Never say 'the user said'.\n"
                    "- Never say 'the user stated'.\n"
                    "- Never say 'according to memory'.\n"
                    "- Never say 'stored in long-term memory'.\n"
                    "- Speak directly to the person using "
                    "'you' and 'your'.\n"
                    "- Keep answers natural and concise.\n"
                    "- Do not repeat yourself."
                ),
            }
        ]

        if context:

            for message in context:

                role = message.get("role")
                content = message.get("content")

                if role not in {
                    "system",
                    "user",
                    "assistant",
                }:
                    continue

                if not content:
                    continue

                messages.append(
                    {
                        "role": role,
                        "content": str(content),
                    }
                )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model_id,
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 300,
        }

        try:

            response = requests.post(
                GROQ_API_URL,
                headers=headers,
                json=payload,
                timeout=60,
            )

            response.raise_for_status()

            data = response.json()

            choices = data.get("choices", [])

            if not choices:
                return "Groq returned no response."

            message = choices[0].get(
                "message",
                {},
            )

            content = message.get("content")

            if not content:
                return "Groq returned an empty response."

            return self.clean_response(content)

        except requests.exceptions.Timeout:

            return "Groq request timed out."

        except requests.exceptions.RequestException as error:

            return f"Groq request failed: {error}"

        except Exception as error:

            return f"AI error: {error}"

    @staticmethod
    def clean_response(
        response: str,
    ) -> str:
        """
        Clean unnecessary AI prefixes
        and repeated whitespace.
        """

        if not response:
            return ""

        response = response.strip()

        prefixes = [
            "Answer:",
            "ANSWER:",
            "PhantomAI:",
            "Phantom AI:",
        ]

        for prefix in prefixes:

            if response.startswith(prefix):

                response = (
                    response[
                        len(prefix):
                    ]
                    .strip()
                )

        lines = []

        for line in response.splitlines():

            line = line.strip()

            if not line:
                continue

            if line not in lines:
                lines.append(line)

        return " ".join(lines).strip()