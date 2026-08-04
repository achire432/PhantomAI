"""
MEMORY ROUTER
==============
Purpose: Handle memory API requests.

Endpoints:
- POST /memory/ - Store a memory
- GET /memory/{key} - Get a memory
- GET /memory/ - Get all memories
- GET /memory/search/{query} - Search memories
- PUT /memory/{key} - Update a memory
- DELETE /memory/{key} - Delete a memory
- GET /memory/for-ai - Memory summary for AI

Why This Matters:
- Exposes memory functionality to users
- All requests require authentication
- Creates a personalized experience
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.schemas.memory import MemoryCreate, MemoryUpdate, MemoryResponse
from backend.app.services.memory_service import (
    store_memory, get_memory, get_all_memories, search_memories,
    update_memory, delete_memory, remember_for_ai
)

router = APIRouter(prefix="/memory", tags=["Memory"])

@router.post("/", response_model=MemoryResponse)
def create_memory(
    memory: MemoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Store a new memory."""
    return store_memory(db, current_user.id, memory)

@router.get("/", response_model=list[MemoryResponse])
def list_memories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all memories for the current user."""
    return get_all_memories(db, current_user.id)

@router.get("/{key}", response_model=MemoryResponse)
def get_memory_by_key(
    key: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific memory by key."""
    memory = get_memory(db, current_user.id, key)
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    return memory

@router.get("/search/{query}", response_model=list[MemoryResponse])
def search_memories_by_query(
    query: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search memories by key or value."""
    return search_memories(db, current_user.id, query)

@router.put("/{key}", response_model=MemoryResponse)
def update_memory_by_key(
    key: str,
    memory: MemoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an existing memory."""
    updated = update_memory(db, current_user.id, key, memory)
    if not updated:
        raise HTTPException(status_code=404, detail="Memory not found")
    return updated

@router.delete("/{key}")
def delete_memory_by_key(
    key: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a memory."""
    if not delete_memory(db, current_user.id, key):
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"message": "Memory deleted successfully"}

@router.get("/for-ai")
def memory_for_ai(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get memory summary for AI integration."""
    return {
        "summary": remember_for_ai(db, current_user.id)
    }