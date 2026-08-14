"""
PHANTOM AI CODE ENGINE
======================

Central orchestration layer for PhantomAI's code-analysis system.

Responsibilities:
1. Read source code.
2. Detect the programming language.
3. Perform deterministic analysis.
4. Optionally send the code to PhantomAI's AI engine.
5. Return one unified result.

This service NEVER executes the supplied source code.
"""

import os
from typing import Optional

from backend.app.services.code.universal_analyzer import (
    analyze_code,
)

from backend.app.services.code.ai_code_analyzer import (
    analyze_code_with_ai,
)


# ============================================================
# SUPPORTED TASKS
# ============================================================

SUPPORTED_TASKS = {
    "explain",
    "bugs",
    "debug",
    "review",
    "improve",
    "security",
    "optimize",
    "architecture",
    "documentation",
}


# ============================================================
# READ SOURCE CODE
# ============================================================

def read_source_code(file_path: str) -> dict:
    """
    Read source code from a file.

    This function only reads text.
    It does not execute the file.
    """

    try:

        if not file_path:
            return {
                "success": False,
                "error": "File path is required.",
            }

        if not os.path.isfile(file_path):
            return {
                "success": False,
                "error": f"File not found: {file_path}",
            }

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:

            content = file.read()

        return {
            "success": True,
            "content": content,
        }

    except UnicodeDecodeError:

        return {
            "success": False,
            "error": "File is not valid UTF-8 text.",
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error),
        }


# ============================================================
# NORMALIZE TASK
# ============================================================

def normalize_task(task: Optional[str]) -> str:
    """
    Normalize the requested analysis task.
    """

    if not task:
        return "explain"

    task = task.strip().lower()

    aliases = {
        "find bugs": "bugs",
        "bug": "bugs",
        "find bug": "bugs",
        "debugging": "debug",
        "code review": "review",
        "improvement": "improve",
        "security analysis": "security",
        "optimization": "optimize",
        "docs": "documentation",
        "document": "documentation",
    }

    task = aliases.get(
        task,
        task,
    )

    if task not in SUPPORTED_TASKS:
        return "explain"

    return task


# ============================================================
# BUILD AI TASK DESCRIPTION
# ============================================================

def build_task_description(task: str) -> str:
    """
    Convert an internal task name into a clear AI instruction.
    """

    descriptions = {
        "explain": (
            "Explain what this code does, how its main parts "
            "work, and how the components relate to each other."
        ),

        "bugs": (
            "Identify possible bugs, errors, incorrect logic, "
            "and problematic implementation choices."
        ),

        "debug": (
            "Analyze the code for debugging purposes. Identify "
            "likely causes of errors and explain how they can "
            "be diagnosed and fixed."
        ),

        "review": (
            "Perform a professional code review. Examine "
            "correctness, readability, maintainability, "
            "structure, and design."
        ),

        "improve": (
            "Suggest practical improvements to the code while "
            "preserving its intended functionality."
        ),

        "security": (
            "Analyze the code for potential security weaknesses, "
            "unsafe behavior, injection risks, authentication "
            "problems, data exposure, and other security concerns."
        ),

        "optimize": (
            "Analyze the code for performance and efficiency "
            "improvements."
        ),

        "architecture": (
            "Analyze the architecture and structure of the "
            "code. Explain responsibilities, dependencies, "
            "coupling, and possible architectural improvements."
        ),

        "documentation": (
            "Explain what documentation should be added and "
            "produce useful documentation guidance for this code."
        ),
    }

    return descriptions.get(
        task,
        descriptions["explain"],
    )


# ============================================================
# MAIN CODE ENGINE
# ============================================================

def run_code_analysis(
    file_path: str,
    task: str = "explain",
    use_ai: bool = True,
    model_name: Optional[str] = None,
) -> dict:
    """
    Run PhantomAI's complete code-analysis pipeline.

    Parameters:
        file_path:
            Path to the source file.

        task:
            Requested analysis operation.

        use_ai:
            Whether to send the source code to the AI engine.

        model_name:
            Optional model to use.

    Returns:
        Unified code-analysis result.
    """

    # --------------------------------------------------------
    # NORMALIZE TASK
    # --------------------------------------------------------

    normalized_task = normalize_task(task)

    # --------------------------------------------------------
    # READ SOURCE
    # --------------------------------------------------------

    source_result = read_source_code(
        file_path
    )

    if not source_result.get("success"):

        return {
            "success": False,
            "error": source_result.get(
                "error",
                "Unable to read source file.",
            ),
        }

    code = source_result["content"]

    # --------------------------------------------------------
    # RUN DETERMINISTIC ANALYSIS
    # --------------------------------------------------------

    static_result = analyze_code(
        file_path
    )

    if not static_result.get("success"):

        return {
            "success": False,
            "error": static_result.get(
                "error",
                "Code analysis failed.",
            ),
            "file": {
                "path": file_path,
            },
        }

    # --------------------------------------------------------
    # GET LANGUAGE
    # --------------------------------------------------------

    file_information = static_result.get(
        "file",
        {},
    )

    language = file_information.get(
        "language",
        "unknown",
    )

    # --------------------------------------------------------
    # BUILD RESULT
    # --------------------------------------------------------

    result = {
        "success": True,

        "file": file_information,

        "analysis": static_result.get(
            "analysis",
            {},
        ),

        "task": normalized_task,

        "capabilities": static_result.get(
            "capabilities",
            {},
        ),

        "ai": {
            "requested": use_ai,
            "success": False,
            "response": None,
            "model": model_name,
        },
    }

    # --------------------------------------------------------
    # AI ANALYSIS
    # --------------------------------------------------------

    if use_ai:

        ai_task = build_task_description(
            normalized_task
        )

        try:

            ai_response = analyze_code_with_ai(
                code=code,
                language=language,
                task=ai_task,
                model_name=model_name,
            )

            result["ai"] = {
                "requested": True,
                "success": True,
                "response": ai_response,
                "model": model_name,
            }

        except Exception as error:

            result["ai"] = {
                "requested": True,
                "success": False,
                "response": None,
                "model": model_name,
                "error": str(error),
            }

    # --------------------------------------------------------
    # UPDATE CAPABILITIES
    # --------------------------------------------------------

    result["capabilities"] = {
        **result["capabilities"],
        "ai_analysis": (
            result["ai"]["success"]
        ),
    }

    # --------------------------------------------------------
    # FINAL MESSAGE
    # --------------------------------------------------------

    result["message"] = (
        "PhantomAI code analysis completed."
    )

    return result


# ============================================================
# SIMPLE ANALYSIS
# ============================================================

def analyze_file(
    file_path: str,
) -> dict:
    """
    Perform deterministic analysis without AI.

    Useful when the caller only wants:
    - language detection
    - syntax analysis
    - functions
    - classes
    - imports
    - variables
    """

    return run_code_analysis(
        file_path=file_path,
        task="explain",
        use_ai=False,
    )


# ============================================================
# AI EXPLANATION
# ============================================================

def explain_file(
    file_path: str,
    model_name: Optional[str] = None,
) -> dict:
    """
    Explain a source file using PhantomAI AI.
    """

    return run_code_analysis(
        file_path=file_path,
        task="explain",
        use_ai=True,
        model_name=model_name,
    )


# ============================================================
# BUG ANALYSIS
# ============================================================

def find_bugs(
    file_path: str,
    model_name: Optional[str] = None,
) -> dict:
    """
    Analyze a source file for possible bugs.
    """

    return run_code_analysis(
        file_path=file_path,
        task="bugs",
        use_ai=True,
        model_name=model_name,
    )


# ============================================================
# SECURITY ANALYSIS
# ============================================================

def security_scan(
    file_path: str,
    model_name: Optional[str] = None,
) -> dict:
    """
    Analyze a source file for security weaknesses.
    """

    return run_code_analysis(
        file_path=file_path,
        task="security",
        use_ai=True,
        model_name=model_name,
    )


# ============================================================
# CODE REVIEW
# ============================================================

def review_file(
    file_path: str,
    model_name: Optional[str] = None,
) -> dict:
    """
    Perform an AI-powered code review.
    """

    return run_code_analysis(
        file_path=file_path,
        task="review",
        use_ai=True,
        model_name=model_name,
    )