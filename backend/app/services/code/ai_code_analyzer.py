"""
PHANTOM AI AI CODE ANALYZER
============================
"""

from typing import Optional

from backend.app.services.multi_ai_service import (
    ask_ai_with_model,
)


def analyze_code_with_ai(
    code: str,
    language: str,
    task: str = "explain",
    model_name: Optional[str] = None,
) -> str:
    """
    Ask PhantomAI's AI engine to analyze source code.
    """

    if not code or not code.strip():
        return "No source code was provided."

    if not language:
        language = "unknown"

    if not task:
        task = "explain"

    prompt = (
        "You are PhantomAI's software engineering engine.\n\n"
        "Your job is to analyze source code and provide "
        "accurate and practical software-engineering assistance.\n\n"
        "Programming language: "
        + language
        + "\n\n"
        "Requested task: "
        + task
        + "\n\n"
        "Rules:\n"
        "1. Do not execute the supplied source code.\n"
        "2. Do not invent behavior that is not supported by the code.\n"
        "3. Do not expose hidden reasoning or chain-of-thought.\n"
        "4. Explain conclusions clearly and directly.\n"
        "5. If something cannot be determined, say so.\n"
        "6. If you identify a problem, explain where it occurs and why.\n"
        "7. When suggesting changes, provide practical solutions.\n"
        "8. Preserve the original programming language.\n\n"
        "SOURCE CODE:\n\n"
        "----- BEGIN SOURCE CODE -----\n"
        + code
        + "\n"
        "----- END SOURCE CODE -----\n\n"
        "Perform the requested task and return a clear, useful answer."
    )

    try:
        if model_name:
            response = ask_ai_with_model(
                prompt=prompt,
                model_name=model_name,
            )
        else:
            response = ask_ai_with_model(
                prompt=prompt,
            )

        if response is None:
            return "The AI model returned no response."

        return str(response).strip()

    except Exception as error:
        return (
            "PhantomAI AI code analysis failed: "
            + str(error)
        )