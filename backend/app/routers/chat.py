# This file handles chat messages from users
# Think of it as the "waiter" in our restaurant

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.schemas.message import MessageCreate, MessageResponse
from backend.app.services.conversation import get_conversation, add_message, get_messages
from backend.app.services.ai import ask_ai  # This is our chef!

# Create a router for chat endpoints
router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("/{conversation_id}/send", response_model=MessageResponse)
def send_message(
    conversation_id: int,
    message: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send a message to Phantom AI and get a response.
    
    How it works:
    1. Check the conversation exists
    2. Save the user's message to the database
    3. Get conversation history for context
    4. Get the AI's response (with context!)
    5. Save the AI's response
    6. Return the AI's response
    """
    
    # 1. Check the conversation exists
    conversation = get_conversation(db, conversation_id, current_user)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # 2. Save the user's message
    user_message = add_message(db, conversation_id, message)
    
    # 3. Get ALL messages for context (this is the memory!)
    all_messages = get_messages(db, conversation_id)
    context = [
        {"role": msg.role, "content": msg.content}
        for msg in all_messages  # All messages, not just the last 10!
    ]
    
    # 4. Get the AI's response WITH context
    ai_response = ask_ai(message.content, context)  # ← Now sends history!
    
    # 5. Save the AI's response
    ai_message = MessageCreate(
        role="assistant",
        content=ai_response
    )
    saved_ai_message = add_message(db, conversation_id, ai_message)
    
    # 6. Return the AI's response
    return saved_ai_message