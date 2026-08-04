"""
NOTES SERVICE
==============

What This File Does:
- Creates new notes
- Retrieves notes for a user
- Updates existing notes
- Deletes notes

Why We Need This:
- Keeps the router clean (routes just call these functions)
- Reusable logic across different parts of the app
- Easy to test
"""

from sqlalchemy.orm import Session
from backend.app.models.note import Note
from backend.app.schemas.note import NoteCreate, NoteUpdate
from datetime import datetime

def create_note(db: Session, user_id: int, note_data: NoteCreate) -> Note:
    """Create a new note for a user."""
    note = Note(user_id=user_id, title=note_data.title, content=note_data.content)
    db.add(note)      # Add to database session
    db.commit()       # Save to database
    db.refresh(note)  # Get the auto-generated ID
    return note

def get_notes(db: Session, user_id: int, search: str = None) -> list:
    """Get all notes for a user."""
    query = db.query(Note).filter(Note.user_id == user_id)
    if search:
        # Search in both title and content
        query = query.filter(
            Note.title.ilike(f"%{search}%") | 
            Note.content.ilike(f"%{search}%")
        )
    return query.order_by(Note.created_at.desc()).all()

def get_note(db: Session, note_id: int, user_id: int) -> Note:
    """Get a specific note by ID."""
    return db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()

def update_note(db: Session, note_id: int, user_id: int, note_data: NoteUpdate) -> Note:
    """Update an existing note."""
    note = get_note(db, note_id, user_id)
    if not note:
        return None
    if note_data.title is not None:
        note.title = note_data.title
    if note_data.content is not None:
        note.content = note_data.content
    note.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(note)
    return note

def delete_note(db: Session, note_id: int, user_id: int) -> bool:
    """Delete a note."""
    note = get_note(db, note_id, user_id)
    if not note:
        return False
    db.delete(note)
    db.commit()
    return True