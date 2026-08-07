import os
from typing import Optional, List, Dict

import requests

from backend.app.models.ai_models import model_registry


GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def ask_ai_with_model(
    prompt: str,
    context: Optional[List[Dict]] = None,
    model_name: Optional[str] = None,
) -> str:
    """
    Main AI router.

    Routes requests to the selected AI model.
    """

    if model_name:
        active_model = model_registry.models.get(model_name)
    else:
        active_model = model_registry.get_active()

    if not active_model:
        return "No active AI model is configured."

    if active_model.provider == "Groq":
        return ask_groq(
            prompt=prompt,
            context=context,
            model=active_model.name,
        )

    if active_model.provider == "Local":
        from backend.app.services.ai import ask_ai as ask_local_ai

        return ask_local_ai(
            prompt=prompt,
            context=context,
        )

    return f"AI provider '{active_model.provider}' is not supported."


def ask_groq(
    prompt: str,
    context: Optional[List[Dict]] = None,
    model: str = "groq-llama3",
) -> str:
    """
    Send a request to Groq.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "GROQ_API_KEY is not configured."

    model_map = {
        "groq-llama3": "llama-3.1-8b-instant",
        "groq-mixtral": "mixtral-8x7b-32768",
    }

    model_id = model_map.get(
        model,
        "llama-3.1-8b-instant",
    )

    messages = [
        {
            "role": "system",
            "content": (
                "CORE RULES:\n"
            "- Answer the user's question directly.\n"
            "- Use supplied long-term memory when relevant.\n"
            "- Long-term memory represents the user's current "
            "known preferences, goals, projects, and facts.\n"
            "- If conversation history conflicts with long-term "
            "memory, prefer long-term memory.\n"
            "- If the latest user message updates an old fact, "
            "treat the latest value as current.\n"
            "- Never invent personal information.\n"
            "- Do not expose internal memory mechanisms unless "
            "the user explicitly asks.\n"
            "- Never say 'the user said'.\n"
            "- Never say 'the user stated'.\n"
            "- Never say 'according to memory'.\n"
            "- Never say 'stored in long-term memory'.\n"
            "- Speak directly to the person using 'you' and 'your'.\n"
            "- Keep answers natural and concise.\n"
            "- Do not repeat yourself."
            ),
        }
    ]

    if context:
        for message in context:
            role = message.get("role")
            content = message.get("content")

            if role not in {"system", "user", "assistant"}:
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

        message = choices[0].get("message", {})

        content = message.get("content")

        if not content:
            return "Groq returned an empty response."

        return clean_response(content)

    except requests.exceptions.Timeout:
        return "Groq request timed out."

    except requests.exceptions.RequestException as error:
        return f"Groq request failed: {error}"

    except Exception as error:
        return f"AI error: {error}"


def clean_response(response: str) -> str:
    """
    Clean unnecessary AI prefixes and repeated whitespace.
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
            response = response[len(prefix):].strip()

    lines = []

    for line in response.splitlines():
        line = line.strip()

        if not line:
            continue

        if line not in lines:
            lines.append(line)

    return " ".join(lines).strip()