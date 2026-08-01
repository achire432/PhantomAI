from sqlalchemy.orm import Session
from datetime import datetime

from backend.app.models.conversation import Conversation
from backend.app.models.message import Message
from backend.app.models.user import User
from backend.app.schemas.conversation import ConversationCreate
from backend.app.schemas.message import MessageCreate

def create_conversation(db: Session, user: User, title: str = None) -> Conversation:
    conversation = Conversation(
        user_id=user.id,
        title=title or f"Conversation {user.id}"
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

def get_conversations(db: Session, user: User) -> list:
    return db.query(Conversation).filter(Conversation.user_id == user.id).order_by(Conversation.updated_at.desc()).all()

def get_conversation(db: Session, conversation_id: int, user: User) -> Conversation:
    return db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user.id
    ).first()

def add_message(db: Session, conversation_id: int, message: MessageCreate) -> Message:
    new_message = Message(
        conversation_id=conversation_id,
        role=message.role,
        content=message.content
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if conversation:
        conversation.updated_at = datetime.utcnow()
        db.commit()
    
    return new_message

def get_messages(db: Session, conversation_id: int) -> list:
    return db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()).all()