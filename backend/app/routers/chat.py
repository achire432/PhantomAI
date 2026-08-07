
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.models.conversation import Conversation
from backend.app.schemas.message import (
    MessageCreate,
    MessageResponse,
)
from backend.app.services.conversation import add_message
from backend.app.services.multi_ai_service import ask_ai_with_model
from backend.app.services.memory_service import remember_for_ai
from backend.app.services.auto_memory_service import (
    process_automatic_memory,
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "/{conversation_id}/send",
    response_model=MessageResponse,
)
def send_message(
    conversation_id: int,
    message: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Send a message to PhantomAI.

    Flow:

    1. Verify conversation ownership.
    2. Save the user's message.
    3. Extract/update long-term memory.
    4. Load fresh long-term memory.
    5. Load conversation history.
    6. Send everything to the AI.
    7. Save the AI response.
    """

    # ========================================================
    # FIND CONVERSATION
    # ========================================================

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id,
        )
        .first()
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    # ========================================================
    # SAVE USER MESSAGE FIRST
    # ========================================================

    add_message(
        db,
        conversation,
        message,
    )

    # ========================================================
    # AUTOMATIC MEMORY EXTRACTION
    # ========================================================

    try:
        process_automatic_memory(
            db=db,
            user_id=current_user.id,
            user_message=message.content,
        )

    except Exception as error:
        print(
            "Automatic memory processing failed:",
            error,
        )

    # ========================================================
    # GET FRESH LONG-TERM MEMORY
    # ========================================================

    long_term_memory = remember_for_ai(
        db,
        current_user.id,
    )

    # ========================================================
    # GET CONVERSATION HISTORY
    # ========================================================

    previous_messages = []

    for msg in conversation.messages:
        previous_messages.append(
            {
                "role": msg.role,
                "content": msg.content,
            }
        )

    # ========================================================
    # BUILD MEMORY CONTEXT
    # ========================================================

    memory_context = {
        "role": "system",
        "content": f"""
You are PhantomAI, a helpful personal AI assistant.

LONG-TERM USER MEMORY

The following information represents the user's current
long-term memory:

{long_term_memory}

MEMORY RULES

1. Use long-term memory when it is relevant.

2. Long-term memory represents stable information that
   the user has explicitly shared or that PhantomAI has
   determined is appropriate to remember.

3. If a newer user message clearly changes an existing
   preference, goal, project, or personal fact, treat the
   newer information as the current value.

4. Do not argue with the user because an older memory
   contains a different value.

5. Do not invent personal information.

6. Never expose internal memory mechanisms unless the
   user explicitly asks how memory works.

7. Never say:
   "the user said"
   "the user stated"
   "according to memory"
   "according to your long-term memory"
   "stored in long-term memory"

8. Speak directly and naturally to the user.

9. If the user asks about a remembered fact, answer
   directly.

10. If the user explicitly asks PhantomAI to remember
    something, acknowledge it naturally.

11. If the user gives a temporary instruction such as:
    "For this conversation, call me Captain"
    do not treat that as a permanent personal fact.

12. Do not claim that temporary conversation instructions
    are permanent memories.

EXAMPLE

Memory:
favorite_color = purple

User:
"What is my favorite color?"

Correct:
"Your favorite color is purple."

Incorrect:
"The user's favorite color is purple."

Incorrect:
"According to your long-term memory, your favorite
color is purple."
""",
    }

    # ========================================================
    # BUILD FULL CONTEXT
    # ========================================================

    full_context = [
        memory_context,
        *previous_messages,
    ]

    # ========================================================
    # ASK AI
    # ========================================================

    ai_response = ask_ai_with_model(
        prompt=message.content,
        context=full_context,
    )

    # ========================================================
    # SAVE ASSISTANT RESPONSE
    # ========================================================

    assistant_message = MessageCreate(
        role="assistant",
        content=ai_response,
    )

    saved_response = add_message(
        db,
        conversation,
        assistant_message,
    )

    return saved_response
