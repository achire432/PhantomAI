"""
NOTES ROUTER
============

Purpose: Handle API requests for notes.

What This File Does:
- POST /notes/ - Create a note
- GET /notes/ - Get all notes
- GET /notes/{id} - Get one note
- PUT /notes/{id} - Update a note
- DELETE /notes/{id} - Delete a note

Why We Need This:
- Users need to save information
- Each note belongs to a user
- All requests require authentication
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from backend.app.services.notes_service import (
    create_note, get_notes, get_note, update_note, delete_note
)

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.post("/", response_model=NoteResponse)
def create_new_note(
    note: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new note."""
    return create_note(db, current_user.id, note)

@router.get("/", response_model=list[NoteResponse])
def list_notes(
    search: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all notes for the current user."""
    return get_notes(db, current_user.id, search)

@router.get("/{note_id}", response_model=NoteResponse)
def get_note_by_id(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific note by ID."""
    note = get_note(db, note_id, current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=NoteResponse)
def update_existing_note(
    note_id: int,
    note: NoteUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an existing note."""
    updated = update_note(db, note_id, current_user.id, note)
    if not updated:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated

@router.delete("/{note_id}")
def delete_existing_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a note."""
    if not delete_note(db, note_id, current_user.id):
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}