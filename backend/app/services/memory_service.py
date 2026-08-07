from datetime import datetime
from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.app.models.memory import Memory
from backend.app.schemas.memory import MemoryCreate, MemoryUpdate


def store_memory(
    db: Session,
    user_id: int,
    memory_data: MemoryCreate
) -> Memory:
    memory = Memory(
        user_id=user_id,
        key=memory_data.key,
        value=memory_data.value,
        category=memory_data.category,
        importance=memory_data.importance,
        expires_at=memory_data.expires_at,
        source="user"
    )

    db.add(memory)
    db.commit()
    db.refresh(memory)

    return memory


def get_memory(
    db: Session,
    user_id: int,
    key: str
) -> Memory:
    return db.query(Memory).filter(
        Memory.user_id == user_id,
        Memory.key == key
    ).first()


def get_all_memories(
    db: Session,
    user_id: int
) -> list[Memory]:
    now = datetime.utcnow()

    return db.query(Memory).filter(
        Memory.user_id == user_id,
        or_(
            Memory.expires_at.is_(None),
            Memory.expires_at > now
        )
    ).order_by(
        Memory.importance.desc(),
        Memory.updated_at.desc()
    ).all()


def search_memories(
    db: Session,
    user_id: int,
    query: str
) -> list[Memory]:
    now = datetime.utcnow()

    return db.query(Memory).filter(
        Memory.user_id == user_id,
        or_(
            Memory.expires_at.is_(None),
            Memory.expires_at > now
        ),
        or_(
            Memory.key.ilike(f"%{query}%"),
            Memory.value.ilike(f"%{query}%"),
            Memory.category.ilike(f"%{query}%")
        )
    ).order_by(
        Memory.importance.desc(),
        Memory.updated_at.desc()
    ).all()


def update_memory(
    db: Session,
    user_id: int,
    key: str,
    memory_data: MemoryUpdate
) -> Memory | None:
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


def delete_memory(
    db: Session,
    user_id: int,
    key: str
) -> bool:
    memory = get_memory(db, user_id, key)

    if not memory:
        return False

    db.delete(memory)
    db.commit()

    return True


def remember_for_ai(
    db: Session,
    user_id: int
) -> str:
    memories = get_all_memories(db, user_id)

    if not memories:
        return "No stored long-term memories for this user."

    summary_lines = [
        "LONG-TERM MEMORY ABOUT THE USER:",
        ""
    ]

    for memory in memories[:20]:
        summary_lines.append(
            f"- {memory.key}: {memory.value}"
        )

    return "\n".join(summary_lines)