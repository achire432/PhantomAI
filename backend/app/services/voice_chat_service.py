"""
VOICE CHAT SERVICE
===================
Purpose: Connect voice with AI for a complete voice conversation.

Why This Matters:
- Makes PhantomAI feel like a real person
- You speak, PhantomAI speaks back
- JARVIS experience!

How It Works:
1. User speaks → Speech-to-Text
2. Text → AI (Qwen)
3. AI response → Text-to-Speech
4. PhantomAI speaks back
"""

from backend.app.services.voice_service import speech_to_text, text_to_speech
from backend.app.services.ai import ask_ai
from backend.app.services.conversation import create_conversation, add_message, get_messages
from backend.app.schemas.message import MessageCreate
from backend.app.models.user import User
from sqlalchemy.orm import Session


def voice_chat(db: Session, user_id: int, conversation_id: int = None) -> dict:
    """
    Complete voice chat flow.
    
    How It Works:
    1. Listen for user speech
    2. Convert to text
    3. Send to AI
    4. Get AI response
    5. Speak response
    6. Return everything
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
    print(f"📝 You said: {user_text}")
    
    # Step 2: If no conversation, create one
    if not conversation_id:
        user = db.query(User).filter(User.id == user_id).first()
        conversation = create_conversation(
            db, 
            user, 
            f"Voice Chat: {user_text[:30]}..."
        )
        conversation_id = conversation.id
    
    # Step 3: Save user message
    user_message = MessageCreate(role="user", content=user_text)
    add_message(db, conversation_id, user_message)
    
    # Step 4: Get conversation history for context
    all_messages = get_messages(db, conversation_id)
    context = [
        {"role": msg.role, "content": msg.content}
        for msg in all_messages[-10:]
    ]
    
    # Step 5: Get AI response
    ai_response = ask_ai(user_text, context)
    print(f"🤖 AI says: {ai_response}")
    
    # Step 6: Save AI response
    ai_message = MessageCreate(role="assistant", content=ai_response)
    add_message(db, conversation_id, ai_message)
    
    # Step 7: Speak the response
    text_to_speech(ai_response)
    
    return {
        "success": True,
        "user_text": user_text,
        "ai_response": ai_response,
        "conversation_id": conversation_id
    }