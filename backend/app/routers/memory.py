from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.schemas.memory import (
    MemoryCreate,
    MemoryUpdate,
    MemoryResponse
)
from backend.app.services.memory_service import (
    store_memory,
    get_memory,
    get_all_memories,
    search_memories,
    update_memory,
    delete_memory,
    remember_for_ai
)


router = APIRouter(
    prefix="/memory",
    tags=["Memory"]
)


@router.post("/", response_model=MemoryResponse)
def create_memory(
    memory: MemoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return store_memory(
        db,
        current_user.id,
        memory
    )


@router.get("/", response_model=list[MemoryResponse])
def list_memories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_all_memories(
        db,
        current_user.id
    )


@router.get("/search/{query}", response_model=list[MemoryResponse])
def search_memories_by_query(
    query: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return search_memories(
        db,
        current_user.id,
        query
    )


@router.get("/for-ai")
def memory_for_ai(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return {
        "summary": remember_for_ai(
            db,
            current_user.id
        )
    }


@router.get("/{key}", response_model=MemoryResponse)
def get_memory_by_key(
    key: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    memory = get_memory(
        db,
        current_user.id,
        key
    )

    if not memory:
        raise HTTPException(
            status_code=404,
            detail="Memory not found"
        )

    return memory


@router.put("/{key}", response_model=MemoryResponse)
def update_memory_by_key(
    key: str,
    memory: MemoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated = update_memory(
        db,
        current_user.id,
        key,
        memory
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Memory not found"
        )

    return updated


@router.delete("/{key}")
def delete_memory_by_key(
    key: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    deleted = delete_memory(
        db,
        current_user.id,
        key
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Memory not found"
        )

    return {
        "message": "Memory deleted successfully"
    }