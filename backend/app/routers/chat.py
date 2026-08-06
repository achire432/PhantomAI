from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.models.conversation import Conversation
from backend.app.schemas.message import MessageCreate, MessageResponse
from backend.app.services.conversation import add_message
from backend.app.services.ai import ask_ai

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
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    previous_messages = []

    for msg in conversation.messages:
        previous_messages.append({
            "role": msg.role,
            "content": msg.content
        })

    user_message = add_message(
        db,
        conversation,
        message
    )

    previous_messages.append({
        "role": "user",
        "content": message.content
    })

    ai_response = ask_ai(
        prompt=message.content,
        context=previous_messages
    )

    assistant_message = MessageCreate(
    role="assistant",
    content=ai_response
)
    
    

    saved_response = add_message(
        db,
        conversation,
        assistant_message
    )

    return saved_response