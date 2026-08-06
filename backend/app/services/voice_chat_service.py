"""
VOICE CHAT SERVICE
===================
Purpose: Connect voice with AI for a complete voice conversation.

Flow:
1. Speech-to-Text
2. Save user message
3. Load conversation history
4. Send context to AI
5. Save AI response
6. Text-to-Speech
"""

from sqlalchemy.orm import Session

from backend.app.models.user import User
from backend.app.schemas.message import MessageCreate
from backend.app.services.voice_service import (
    speech_to_text,
    text_to_speech,
)
from backend.app.services.ai import ask_ai
from backend.app.services.conversation import (
    create_conversation,
    get_conversation,
    add_message,
    get_messages,
)


def voice_chat(
    db: Session,
    user_id: int,
    conversation_id: int = None
) -> dict:
    """
    Complete voice chat flow.
    """

    # Step 1: Listen to user
    print("🎤 Listening for your command...")

    listen_result = speech_to_text()

    if not listen_result.get("success"):
        return {
            "success": False,
            "error": listen_result.get("error")
        }

    user_text = listen_result.get("text")

    if not user_text:
        return {
            "success": False,
            "error": "No speech detected."
        }

    print(f"📝 You said: {user_text}")

    # Step 2: Get the user
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        return {
            "success": False,
            "error": "User not found."
        }

    # Step 3: Create or verify conversation
    if conversation_id is None:
        conversation = create_conversation(
            db,
            user,
            f"Voice Chat: {user_text[:30]}..."
        )
    else:
        conversation = get_conversation(
            db,
            conversation_id,
            user
        )

        if not conversation:
            return {
                "success": False,
                "error": "Conversation not found."
            }

    # Step 4: Save user message
    user_message = MessageCreate(
        role="user",
        content=user_text
    )

    add_message(
        db,
        conversation,
        user_message
    )

    # Step 5: Get conversation history
    all_messages = get_messages(
        db,
        conversation
    )

    # Keep the latest 10 messages for AI context
    context = [
        {
            "role": msg.role,
            "content": msg.content
        }
        for msg in all_messages[-10:]
    ]

    # Step 6: Ask AI
    ai_response = ask_ai(
        user_text,
        context
    )

    print(f"🤖 AI says: {ai_response}")

    # Step 7: Save AI response
    ai_message = MessageCreate(
        role="assistant",
        content=ai_response
    )

    add_message(
        db,
        conversation,
        ai_message
    )

    # Step 8: Speak AI response
    text_to_speech(ai_response)

    return {
        "success": True,
        "user_text": user_text,
        "ai_response": ai_response,
        "conversation_id": conversation.id
    }
