
import json
import re
from typing import Optional

from sqlalchemy.orm import Session

from backend.app.models.memory import Memory
from backend.app.services.multi_ai_service import ask_groq


# ============================================================
# CANONICAL MEMORY KEYS
# ============================================================

KEY_ALIASES = {
    # Programming language
    "language": "favorite_language",
    "favorite_language": "favorite_language",
    "programming_language": "favorite_language",
    "favorite_programming_language": "favorite_language",

    # Backend framework
    "backend": "favorite_backend",
    "backend_framework": "favorite_backend",
    "favorite_backend": "favorite_backend",
    "favorite_backend_framework": "favorite_backend",

    # Database
    "database": "favorite_database",
    "favorite_database": "favorite_database",
    "preferred_database": "favorite_database",
    "favorite_db": "favorite_database",
    "db": "favorite_database",

    # Project
    "project": "current_project",
    "current_project": "current_project",
    "current_project_name": "current_project",

    # Goals
    "goal": "current_goal",
    "current_goal": "current_goal",

    "learning_goal": "learning_goal",

    # Favorite color
    "favorite_color": "favorite_color",
    "color": "favorite_color",

    # Name
    "name": "name",
    "user_name": "name",
    "username": "name",
}


# ============================================================
# NORMALIZE MEMORY KEY
# ============================================================

def normalize_key(key: str) -> str:
    """
    Normalize a memory key and convert aliases
    into canonical memory keys.
    """

    if not key:
        return ""

    key = key.strip().lower()

    key = re.sub(
        r"[^a-z0-9_ ]+",
        "",
        key,
    )

    key = re.sub(
        r"\s+",
        "_",
        key,
    )

    return KEY_ALIASES.get(
        key,
        key,
    )


# ============================================================
# TEMPORARY INSTRUCTION DETECTION
# ============================================================

def is_temporary_instruction(text: str) -> bool:
    """
    Detect instructions that should only apply to the
    current conversation/session.

    These must NOT become permanent long-term memories.
    """

    if not text:
        return False

    normalized = text.strip().lower()

    temporary_patterns = [
        r"\bfor this conversation\b",
        r"\bin this conversation\b",
        r"\bfor this chat\b",
        r"\bin this chat\b",
        r"\bfor now\b",
        r"\bjust for now\b",
        r"\btemporarily\b",
        r"\bfor the rest of this conversation\b",
        r"\bin this session\b",
        r"\bfor this session\b",
        r"\bcall me\b",
        r"\baddress me as\b",
        r"\brefer to me as\b",
    ]

    return any(
        re.search(
            pattern,
            normalized,
        )
        for pattern in temporary_patterns
    )


# ============================================================
# EXTRACT MEMORY USING GROQ
# ============================================================

def extract_memory(
    text: str,
) -> Optional[dict]:
    """
    Ask Groq to extract ONE stable piece
    of information from the user's message.
    """

    if not text or not text.strip():
        return None

    # ========================================================
    # BLOCK TEMPORARY INSTRUCTIONS
    # ========================================================

    if is_temporary_instruction(text):
        print(
            "🧠 Temporary conversation instruction detected."
        )
        print(
            "🚫 Permanent memory extraction skipped."
        )

        return None

    # ========================================================
    # MEMORY EXTRACTION PROMPT
    # ========================================================

    prompt = f"""
You are PhantomAI's long-term memory extraction engine.

Your ONLY task is to analyze the user's message
and determine whether it contains ONE stable piece
of information worth remembering.

Return ONLY valid JSON.

Do not explain anything.
Do not provide reasoning.
Do not repeat the user's message.
Do not add markdown.
Do not add text before or after the JSON.

If useful memory exists, return:

{{
    "remember": true,
    "key": "short_canonical_key",
    "value": "memory value",
    "category": "fact",
    "importance": 5
}}

If there is no useful long-term memory, return:

{{
    "remember": false
}}

REMEMBER STABLE USER INFORMATION SUCH AS:

- favorite programming language
- favorite color
- favorite database
- preferred technologies
- preferred backend framework
- current project
- current goal
- learning goal
- stable preferences
- stable personal facts
- user's name

DO NOT REMEMBER:

- passwords
- API keys
- authentication tokens
- secrets
- temporary questions
- greetings
- random temporary information
- system instructions
- conversation-specific instructions
- temporary nicknames
- instructions such as "call me X for this conversation"

IMPORTANT:

Only remember information that is actually supported
by the user's message.

Do not infer a reason or relationship that the user
did not explicitly state.

For example, if the user says:

"I am learning FastAPI because I want to become
very good at backend development."

You may remember the learning goal:

"become very good at backend development"

But do NOT invent:

"learning FastAPI is their reason for the goal"

unless explicitly stated.

USE THESE CANONICAL KEYS:

Programming language:
favorite_language

Backend framework:
favorite_backend

Database:
favorite_database

Current project:
current_project

Current goal:
current_goal

Learning goal:
learning_goal

Favorite color:
favorite_color

User name:
name

EXAMPLES:

User:
"My favorite programming language is Python."

Return:

{{
    "remember": true,
    "key": "favorite_language",
    "value": "Python",
    "category": "preference",
    "importance": 8
}}

User:
"I am building a project called PhantomAI."

Return:

{{
    "remember": true,
    "key": "current_project",
    "value": "PhantomAI",
    "category": "project",
    "importance": 8
}}

User:
"I want to learn FastAPI deeply this year."

Return:

{{
    "remember": true,
    "key": "learning_goal",
    "value": "learn FastAPI deeply",
    "category": "goal",
    "importance": 8
}}

User:
"My favorite color is blue."

Return:

{{
    "remember": true,
    "key": "favorite_color",
    "value": "blue",
    "category": "preference",
    "importance": 8
}}

User:
"My favorite database is PostgreSQL."

Return:

{{
    "remember": true,
    "key": "favorite_database",
    "value": "PostgreSQL",
    "category": "preference",
    "importance": 8
}}

User:
"What is FastAPI?"

Return:

{{
    "remember": false
}}

USER MESSAGE:

{text}
"""

    # ========================================================
    # ASK GROQ
    # ========================================================

    try:
        response = ask_groq(
            prompt=prompt,
            context=None,
            model="groq-llama3",
        )

        print(
            "\n🧠 Groq memory extractor response:"
        )
        print(response)

        if not response:
            return None

        # ====================================================
        # EXTRACT JSON FROM RESPONSE
        # ====================================================

        start = response.find("{")
        end = response.rfind("}")

        if start == -1 or end == -1:
            print(
                "❌ Groq did not return valid JSON."
            )
            return None

        json_text = response[
            start:end + 1
        ]

        # ====================================================
        # PARSE JSON
        # ====================================================

        try:
            data = json.loads(
                json_text
            )

        except json.JSONDecodeError as error:
            print(
                "❌ Memory JSON parsing failed:",
                error,
            )
            return None

        # ====================================================
        # NO MEMORY
        # ====================================================

        if not data.get("remember"):
            print(
                "🧠 No stable memory detected."
            )
            return None

        # ====================================================
        # EXTRACT FIELDS
        # ====================================================

        key = normalize_key(
            str(
                data.get(
                    "key",
                    "",
                )
            )
        )

        value = str(
            data.get(
                "value",
                "",
            )
        ).strip()

        category = str(
            data.get(
                "category",
                "fact",
            )
        ).strip().lower()

        importance = data.get(
            "importance",
            5,
        )

        # ====================================================
        # VALIDATE KEY/VALUE
        # ====================================================

        if not key or not value:
            print(
                "❌ Memory key or value is empty."
            )
            return None

        # ====================================================
        # VALIDATE IMPORTANCE
        # ====================================================

        try:
            importance = int(
                importance
            )

        except (
            TypeError,
            ValueError,
        ):
            importance = 5

        importance = max(
            1,
            min(
                10,
                importance,
            ),
        )

        # ====================================================
        # RETURN MEMORY
        # ====================================================

        return {
            "key": key,
            "value": value,
            "category": category,
            "importance": importance,
        }

    except Exception as error:
        print(
            "❌ Groq automatic memory extraction failed:",
            error,
        )

        return None


# ============================================================
# SAVE / UPDATE AUTOMATIC MEMORY
# ============================================================

def process_automatic_memory(
    db: Session,
    user_id: int,
    user_message: str,
) -> Optional[Memory]:
    """
    Extract memory from a user message and save/update it.

    If the same user already has a memory with the same
    canonical key, update that memory instead of creating
    a duplicate.
    """

    # ========================================================
    # EMPTY MESSAGE
    # ========================================================

    if not user_message or not user_message.strip():
        return None

    # ========================================================
    # TEMPORARY INSTRUCTION
    # ========================================================

    if is_temporary_instruction(
        user_message
    ):
        print(
            "🧠 Temporary instruction detected."
        )
        print(
            "🚫 No permanent memory will be created."
        )

        return None

    # ========================================================
    # EXTRACT MEMORY
    # ========================================================

    memory_data = extract_memory(
        user_message
    )

    if not memory_data:
        return None

    # ========================================================
    # SHOW EXTRACTED MEMORY
    # ========================================================

    print(
        "🧠 Extracted memory:"
    )

    print(
        f"Key: {memory_data['key']}"
    )

    print(
        f"Value: {memory_data['value']}"
    )

    print(
        f"Category: {memory_data['category']}"
    )

    print(
        f"Importance: {memory_data['importance']}"
    )

    # ========================================================
    # FIND EXISTING MEMORY
    # ========================================================

    existing_memory = (
        db.query(Memory)
        .filter(
            Memory.user_id == user_id,
            Memory.key == memory_data["key"],
        )
        .first()
    )

    # ========================================================
    # UPDATE EXISTING MEMORY
    # ========================================================

    if existing_memory:

        print(
            "🧠 Updating memory:"
        )

        print(
            f"{memory_data['key']} "
            f"→ {memory_data['value']}"
        )

        existing_memory.value = (
            memory_data["value"]
        )

        existing_memory.category = (
            memory_data["category"]
        )

        existing_memory.importance = (
            memory_data["importance"]
        )

        existing_memory.source = "ai"

        db.commit()

        db.refresh(
            existing_memory
        )

        return existing_memory

    # ========================================================
    # CREATE NEW MEMORY
    # ========================================================

    print(
        "🧠 Creating new memory:"
    )

    print(
        f"{memory_data['key']} "
        f"→ {memory_data['value']}"
    )

    new_memory = Memory(
        user_id=user_id,
        key=memory_data["key"],
        value=memory_data["value"],
        category=memory_data["category"],
        importance=memory_data["importance"],
        source="ai",
    )

    db.add(
        new_memory
    )

    db.commit()

    db.refresh(
        new_memory
    )

    return new_memory

