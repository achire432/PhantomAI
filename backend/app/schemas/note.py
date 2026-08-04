from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NoteCreate(BaseModel):
    """
    This is what the user sends when creating a note.
    They only need to provide title and content.
    The ID, user_id, and timestamps are auto-generated.
    """
    title: str
    content: str

class NoteUpdate(BaseModel):
    """
    This is what the user sends when updating a note.
    Everything is optional because they might only change one field.
    """
    title: Optional[str] = None
    content: Optional[str] = None

class NoteResponse(BaseModel):
    """
    This is what we return to the user after creating/fetching a note.
    We include all fields so they know what was saved.
    """
    id: int
    user_id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True