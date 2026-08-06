from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.schemas.conversation import (
    ConversationCreate,
    ConversationResponse,
)
from backend.app.schemas.message import (
    MessageCreate,
    MessageResponse,
)
from backend.app.services.conversation import (
    create_conversation,
    get_conversations,
    get_conversation,
    add_message,
    get_messages,
)


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)


@router.post(
    "/",
    response_model=ConversationResponse
)
def new_conversation(
    data: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_conversation(
        db,
        current_user,
        data.title
    )


@router.get(
    "/",
    response_model=list[ConversationResponse]
)
def list_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_conversations(
        db,
        current_user
    )


@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse
)
def get_conversation_details(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conversation = get_conversation(
        db,
        conversation_id,
        current_user
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    return conversation


@router.post(
    "/{conversation_id}/messages",
    response_model=MessageResponse
)
def send_message(
    conversation_id: int,
    message: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify ownership first
    conversation = get_conversation(
        db,
        conversation_id,
        current_user
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    return add_message(
        db,
        conversation,
        message
    )


@router.get(
    "/{conversation_id}/messages",
    response_model=list[MessageResponse]
)
def list_messages(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify ownership first
    conversation = get_conversation(
        db,
        conversation_id,
        current_user
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    return get_messages(
        db,
        conversation
    )
