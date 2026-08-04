"""
MEMORY SERVICE
===============
Purpose: Manage long-term memory for PhantomAI.

Why This Matters:
- PhantomAI remembers important facts
- Creates a knowledge base about you
- Builds a personalized experience

How It Works:
1. Store memories (key-value pairs)
2. Search memories
3. Retrieve memories
4. Update memories
5. Delete memories
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.app.models.memory import Memory
from backend.app.schemas.memory import MemoryCreate, MemoryUpdate
from datetime import datetime

def store_memory(db: Session, user_id: int, memory_data: MemoryCreate) -> Memory:
    """
    Store a new memory.
    
    Example:
        store_memory(db, 2, MemoryCreate(key="project", value="PhantomAI"))
    """
    memory = Memory(
        user_id=user_id,
        key=memory_data.key,
        value=memory_data.value,
        category=memory_data.category,
        importance=memory_data.importance,
        expires_at=memory_data.expires_at
    )
    db.add(memory)
    db.commit()
    db.refresh(memory)
    return memory

def get_memory(db: Session, user_id: int, key: str) -> Memory:
    """
    Get a specific memory by key.
    """
    return db.query(Memory).filter(
        Memory.user_id == user_id,
        Memory.key == key
    ).first()

def get_all_memories(db: Session, user_id: int) -> list:
    """
    Get all memories for a user.
    """
    return db.query(Memory).filter(
        Memory.user_id == user_id
    ).order_by(Memory.importance.desc()).all()

def search_memories(db: Session, user_id: int, query: str) -> list:
    """
    Search memories by key or value.
    """
    return db.query(Memory).filter(
        Memory.user_id == user_id,
        or_(
            Memory.key.ilike(f"%{query}%"),
            Memory.value.ilike(f"%{query}%")
        )
    ).order_by(Memory.importance.desc()).all()

def update_memory(db: Session, user_id: int, key: str, memory_data: MemoryUpdate) -> Memory:
    """
    Update an existing memory.
    """
    memory = get_memory(db, user_id, key)
    if not memory:
        return None
    
    if memory_data.value is not None:
        memory.value = memory_data.value
    if memory_data.importance is not None:
        memory.importance = memory_data.importance
    if memory_data.expires_at is not None:
        memory.expires_at = memory_data.expires_at
    
    memory.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(memory)
    return memory

def delete_memory(db: Session, user_id: int, key: str) -> bool:
    """
    Delete a memory by key.
    """
    memory = get_memory(db, user_id, key)
    if not memory:
        return False
    db.delete(memory)
    db.commit()
    return True

def remember_for_ai(db: Session, user_id: int) -> str:
    """
    Generate a memory summary for AI prompts.
    """
    memories = get_all_memories(db, user_id)
    if not memories:
        return "No stored memories."
    
    summary = "Here are the memories this user has stored:\n\n"
    for mem in memories[:10]:  # Only top 10 most important
        summary += f"- {mem.key}: {mem.value} (importance: {mem.importance})\n"
    
    return summary