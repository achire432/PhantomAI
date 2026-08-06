from datetime import datetime

from sqlalchemy.orm import Session

from backend.app.models.conversation import Conversation
from backend.app.models.message import Message
from backend.app.models.user import User
from backend.app.schemas.message import MessageCreate


def create_conversation(
    db: Session,
    user: User,
    title: str = None
) -> Conversation:
    """
    Create a conversation owned by the authenticated user.
    """

    conversation = Conversation(
        user_id=user.id,
        title=title or f"Conversation {user.id}"
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def get_conversations(
    db: Session,
    user: User
) -> list[Conversation]:
    """
    Return only conversations belonging to the authenticated user.
    """

    return (
        db.query(Conversation)
        .filter(Conversation.user_id == user.id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )


def get_conversation(
    db: Session,
    conversation_id: int,
    user: User
) -> Conversation | None:
    """
    Get one conversation only if it belongs to the authenticated user.
    """

    return (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user.id
        )
        .first()
    )


def add_message(
    db: Session,
    conversation: Conversation,
    message: MessageCreate
) -> Message:
    """
    Add a message to an already-authorized conversation.

    IMPORTANT:
    The caller must first obtain the conversation using
    get_conversation(), which verifies ownership.
    """

    new_message = Message(
        conversation_id=conversation.id,
        role=message.role,
        content=message.content
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    conversation.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(conversation)

    return new_message


def get_messages(
    db: Session,
    conversation: Conversation
) -> list[Message]:
    """
    Get messages belonging to an already-authorized conversation.
    """

    return (
        db.query(Message)
        .filter(Message.conversation_id == conversation.id)
        .order_by(Message.created_at.asc())
        .all()
    )
