"""
PHANTOM AI CODE GENERATION SERVICE
===================================

Generates source code using PhantomAI's existing
multi-model AI service.

This service does NOT write files.

It only generates code/content.
"""

from typing import Optional

from backend.app.services.multi_ai_service import (
    ask_ai_with_model,
)


# ============================================================
# CODE GENERATION
# ============================================================

def generate_code(
    prompt: str,
    language: str = "python",
    model_name: Optional[str] = None,
) -> dict:
    """
    Generate source code from a natural-language request.
    """

    if not prompt or not prompt.strip():
        return {
            "success": False,
            "error": "Generation prompt cannot be empty.",
        }

    language = language.strip().lower()

    system_prompt = f"""
You are PhantomAI's professional software engineering engine.

Generate production-quality {language} code.

Requirements:

1. Return only the requested code.
2. Do not explain the code.
3. Do not mention PhantomAI.
4. Do not use markdown fences.
5. Do not invent external requirements unless necessary.
6. Write clean and maintainable code.
7. Follow normal conventions for {language}.
8. Include useful error handling where appropriate.
9. Do not execute the code.
10. Do not claim that the code was tested.

The requested programming language is:

{language}
"""

    full_prompt = f"""
{system_prompt}

USER REQUEST:

{prompt}
"""

    try:

        response = ask_ai_with_model(
            prompt=full_prompt,
            context=[],
            model_name=model_name,
        )

        return {
            "success": True,
            "language": language,
            "prompt": prompt,
            "code": response,
            "model": model_name,
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error),
        }


# ============================================================
# CODE EXPLANATION
# ============================================================

def explain_code(
    code: str,
    language: str = "python",
    model_name: Optional[str] = None,
) -> dict:
    """
    Explain supplied source code.
    """

    if not code.strip():
        return {
            "success": False,
            "error": "Code cannot be empty.",
        }

    prompt = f"""
Analyze the following {language} source code.

Explain:

- What the code does
- Important functions
- Important classes
- Data flow
- Dependencies
- Potential problems
- How the components relate

SOURCE CODE:

{code}
"""

    try:

        response = ask_ai_with_model(
            prompt=prompt,
            context=[],
            model_name=model_name,
        )

        return {
            "success": True,
            "language": language,
            "response": response,
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error),
        }


# ============================================================
# CODE REVIEW
# ============================================================

def review_code(
    code: str,
    language: str = "python",
    model_name: Optional[str] = None,
) -> dict:
    """
    Perform a professional code review.
    """

    prompt = f"""
Perform a professional code review of this {language} code.

Review:

1. Correctness
2. Readability
3. Maintainability
4. Architecture
5. Error handling
6. Performance
7. Security
8. Code smells
9. Potential bugs
10. Recommended improvements

SOURCE CODE:

{code}

Return a structured review.
"""

    try:

        response = ask_ai_with_model(
            prompt=prompt,
            context=[],
            model_name=model_name,
        )

        return {
            "success": True,
            "language": language,
            "response": response,
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error),
        }


# ============================================================
# CODE FIX
# ============================================================

def fix_code(
    code: str,
    language: str = "python",
    problem: str = "",
    model_name: Optional[str] = None,
) -> dict:
    """
    Produce an improved version of supplied code.
    """

    prompt = f"""
You are debugging {language} code.

Problem description:

{problem}

SOURCE CODE:

{code}

Return:

1. A short explanation of the problem.
2. The corrected code.

Do not claim that the code was executed or tested.
"""

    try:

        response = ask_ai_with_model(
            prompt=prompt,
            context=[],
            model_name=model_name,
        )

        return {
            "success": True,
            "language": language,
            "response": response,
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error),
        }