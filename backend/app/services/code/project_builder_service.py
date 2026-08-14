"""
PHANTOM AI PROJECT BUILDER
==========================

AI-powered project planning service.

Converts a natural-language application request into
a structured multi-file project plan.

The AI never writes directly to disk.

The service:
1. Asks the AI to design the project.
2. Extracts the AI response.
3. Repairs common malformed JSON.
4. Validates the project structure.
5. Returns safe file changes.
"""

import json
import re
from typing import Optional

from backend.app.services.multi_ai_service import (
    ask_ai_with_model,
)


# ============================================================
# JSON EXTRACTION
# ============================================================

def extract_json(text: str):
    """
    Extract valid JSON from an AI response.

    Handles:
    - normal JSON
    - markdown JSON fences
    - surrounding text
    """

    if not text:
        return None

    text = text.strip()

    # --------------------------------------------------------
    # Remove markdown fences
    # --------------------------------------------------------

    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"^```\s*",
        "",
        text,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    text = text.strip()

    # --------------------------------------------------------
    # Direct JSON
    # --------------------------------------------------------

    try:
        return json.loads(text)

    except json.JSONDecodeError:
        pass

    # --------------------------------------------------------
    # Find JSON object inside response
    # --------------------------------------------------------

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        return None

    candidate = text[start:end + 1]

    try:
        return json.loads(candidate)

    except json.JSONDecodeError:
        return None


# ============================================================
# MALFORMED FILE ARRAY REPAIR
# ============================================================

def repair_files_array(text: str):
    """
    Attempts to repair the specific malformed structure
    sometimes produced by AI models.

    Example malformed output:

    "files": [
        "action": "create",
        "path": "app.py",
        "content": "..."
    ]

    Correct structure:

    "files": [
        {
            "action": "create",
            "path": "app.py",
            "content": "..."
        }
    ]

    This is intentionally conservative.
    """

    if not text:
        return text

    # --------------------------------------------------------
    # First try normal JSON
    # --------------------------------------------------------

    parsed = extract_json(text)

    if isinstance(parsed, dict):

        files = parsed.get("files")

        if isinstance(files, list):
            return json.dumps(parsed)

    # --------------------------------------------------------
    # Find files section
    # --------------------------------------------------------

    files_match = re.search(
        r'"files"\s*:\s*\[',
        text,
        flags=re.IGNORECASE,
    )

    if not files_match:
        return text

    start = files_match.end()

    # --------------------------------------------------------
    # Find closing array
    # --------------------------------------------------------

    depth = 1
    end = start

    while end < len(text) and depth > 0:

        if text[end] == "[":
            depth += 1

        elif text[end] == "]":
            depth -= 1

        end += 1

    if depth != 0:
        return text

    files_content = text[start:end - 1]

    # --------------------------------------------------------
    # Extract repeated file objects
    # --------------------------------------------------------

    pattern = re.compile(
        r'"action"\s*:\s*"([^"]*)"\s*,\s*'
        r'"path"\s*:\s*"([^"]*)"\s*,\s*'
        r'"content"\s*:\s*"((?:\\.|[^"\\])*)"',
        flags=re.DOTALL,
    )

    matches = pattern.findall(files_content)

    if not matches:
        return text

    files = []

    for action, path, content in matches:

        try:
            decoded_content = json.loads(
                '"' + content + '"'
            )
        except Exception:
            decoded_content = content

        files.append(
            {
                "action": action or "create",
                "path": path,
                "content": decoded_content,
            }
        )

    # --------------------------------------------------------
    # Extract project metadata
    # --------------------------------------------------------

    project_name_match = re.search(
        r'"project_name"\s*:\s*"([^"]*)"',
        text,
    )

    description_match = re.search(
        r'"description"\s*:\s*"((?:\\.|[^"\\])*)"',
        text,
        flags=re.DOTALL,
    )

    project_name = (
        project_name_match.group(1)
        if project_name_match
        else "phantom-project"
    )

    description = ""

    if description_match:

        try:
            description = json.loads(
                '"' + description_match.group(1) + '"'
            )
        except Exception:
            description = description_match.group(1)

    repaired = {
        "project_name": project_name,
        "description": description,
        "files": files,
    }

    return json.dumps(
        repaired,
        ensure_ascii=False,
    )


# ============================================================
# NORMALIZE AI RESPONSE
# ============================================================

def normalize_project_response(
    response: str,
):
    """
    Parse the AI response and attempt repair when necessary.
    """

    # --------------------------------------------------------
    # Try normal JSON first
    # --------------------------------------------------------

    data = extract_json(response)

    if isinstance(data, dict):

        files = data.get("files")

        if isinstance(files, list):

            return data

    # --------------------------------------------------------
    # Attempt repair
    # --------------------------------------------------------

    repaired_text = repair_files_array(
        response
    )

    repaired_data = extract_json(
        repaired_text
    )

    if isinstance(repaired_data, dict):

        if isinstance(
            repaired_data.get("files"),
            list,
        ):

            return repaired_data

    return None


# ============================================================
# VALIDATE PROJECT FILE
# ============================================================

def validate_file_entry(
    file_entry: dict,
):
    """
    Validate one generated project file.
    """

    if not isinstance(
        file_entry,
        dict,
    ):
        return None

    path = str(
        file_entry.get(
            "path",
            "",
        )
    ).strip()

    if not path:
        return None

    # --------------------------------------------------------
    # Never allow absolute paths
    # --------------------------------------------------------

    if path.startswith("/"):
        return None

    if path.startswith("\\"):
        return None

    # --------------------------------------------------------
    # Never allow traversal
    # --------------------------------------------------------

    parts = path.replace(
        "\\",
        "/",
    ).split("/")

    if ".." in parts:
        return None

    # --------------------------------------------------------
    # Normalize action
    # --------------------------------------------------------

    action = str(
        file_entry.get(
            "action",
            "create",
        )
    ).lower().strip()

    allowed_actions = {
        "create",
        "update",
        "delete",
    }

    if action not in allowed_actions:
        action = "create"

    # --------------------------------------------------------
    # Content
    # --------------------------------------------------------

    content = file_entry.get(
        "content",
        "",
    )

    if content is None:
        content = ""

    if not isinstance(
        content,
        str,
    ):
        content = str(content)

    return {
        "action": action,
        "path": path,
        "content": content,
    }


# ============================================================
# GENERATE PROJECT PLAN
# ============================================================

def generate_project_plan(
    prompt: str,
    model_name: Optional[str] = None,
) -> dict:
    """
    Ask PhantomAI to design a complete multi-file project.
    """

    if not prompt or not prompt.strip():

        return {
            "success": False,
            "error": "Project prompt cannot be empty.",
        }

    # ========================================================
    # SYSTEM PROMPT
    # ========================================================

    system_prompt = """
You are PhantomAI's autonomous software architecture engine.

Your job is to design complete software projects from
natural-language descriptions.

IMPORTANT:

You MUST return ONLY valid JSON.

DO NOT return markdown.

DO NOT return ```json.

DO NOT explain anything.

DO NOT write text before or after the JSON.

The JSON MUST follow this EXACT structure:

{
  "project_name": "student-api",
  "description": "A simple student API",
  "files": [
    {
      "action": "create",
      "path": "app.py",
      "content": "complete source code here"
    },
    {
      "action": "create",
      "path": "requirements.txt",
      "content": "Flask\\nSQLAlchemy\\n"
    }
  ]
}

CRITICAL JSON RULE:

The files property MUST be an array of OBJECTS.

CORRECT:

"files": [
  {
    "action": "create",
    "path": "app.py",
    "content": "..."
  }
]

WRONG:

"files": [
  "action": "create",
  "path": "app.py",
  "content": "..."
]

WRONG:

"files": [
  "action": "create",
  "path": "app.py"
]

Every file MUST be enclosed inside { }.

PROJECT RULES:

1. Every file must contain complete usable content.

2. Never use markdown code fences inside file content.

3. Never include commentary outside JSON.

4. All paths must be relative.

5. Never use absolute paths.

6. Never use ../.

7. Never use secrets.

8. Never include API keys.

9. Include important project files.

10. Include README.md when appropriate.

11. Include requirements.txt when appropriate.

12. Keep architecture simple and maintainable.

13. Do not claim that the generated project was tested.

14. Do not execute code.

15. Do not return explanations.

16. Return syntactically valid JSON.

17. Escape newline characters correctly inside JSON strings.

18. Escape double quotes correctly inside JSON strings.

19. The response must begin with { and end with }.
"""

    prompt_text = f"""
{system_prompt}

APPLICATION REQUEST:

{prompt}
"""

    # ========================================================
    # CALL AI
    # ========================================================

    try:

        response = ask_ai_with_model(
            prompt=prompt_text,
            context=[],
            model_name=model_name,
        )

        print()
        print("=" * 60)
        print("PHANTOMAI PROJECT BUILDER AI RESPONSE")
        print("=" * 60)
        print(response)
        print("=" * 60)
        print()

        # ====================================================
        # NORMALIZE RESPONSE
        # ====================================================

        data = normalize_project_response(
            response
        )

        if not isinstance(
            data,
            dict,
        ):

            return {
                "success": False,
                "error": "AI returned invalid project JSON.",
                "raw_response": response,
            }

        # ====================================================
        # PROJECT NAME
        # ====================================================

        project_name = str(
            data.get(
                "project_name",
                "phantom-project",
            )
        ).strip()

        if not project_name:

            project_name = "phantom-project"

        # ====================================================
        # DESCRIPTION
        # ====================================================

        description = str(
            data.get(
                "description",
                "",
            )
        )

        # ====================================================
        # FILES
        # ====================================================

        files = data.get(
            "files",
            [],
        )

        if not isinstance(
            files,
            list,
        ):

            return {
                "success": False,
                "error": (
                    "Project response does not "
                    "contain a valid files list."
                ),
                "raw_response": response,
            }

        validated_files = []

        for file_entry in files:

            validated = validate_file_entry(
                file_entry
            )

            if validated is None:
                continue

            validated_files.append(
                validated
            )

        # ====================================================
        # REQUIRE AT LEAST ONE FILE
        # ====================================================

        if not validated_files:

            return {
                "success": False,
                "error": (
                    "AI generated a project "
                    "without valid files."
                ),
                "raw_response": response,
            }

        # ====================================================
        # SUCCESS
        # ====================================================

        return {
            "success": True,
            "project_name": project_name,
            "description": description,
            "files": validated_files,
            "file_count": len(
                validated_files
            ),
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error),
        }