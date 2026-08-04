"""
CALENDAR ROUTER
================
Purpose: Handle API requests for calendar events.

Endpoints:
- POST /calendar/ - Create an event
- GET /calendar/ - Get all events
- GET /calendar/{id} - Get one event
- PUT /calendar/{id} - Update an event
- DELETE /calendar/{id} - Delete an event
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.schemas.calendar import CalendarEventCreate, CalendarEventUpdate, CalendarEventResponse
from backend.app.services.calendar_service import (
    create_event, get_events, get_event, update_event, delete_event
)

router = APIRouter(prefix="/calendar", tags=["Calendar"])

@router.post("/", response_model=CalendarEventResponse)
def create_new_event(
    event: CalendarEventCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new calendar event."""
    return create_event(db, current_user.id, event)

@router.get("/", response_model=list[CalendarEventResponse])
def list_events(
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all events for the current user."""
    return get_events(db, current_user.id, start, end)

@router.get("/{event_id}", response_model=CalendarEventResponse)
def get_event_by_id(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific event by ID."""
    event = get_event(db, event_id, current_user.id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/{event_id}", response_model=CalendarEventResponse)
def update_existing_event(
    event_id: int,
    event: CalendarEventUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an existing event."""
    updated = update_event(db, event_id, current_user.id, event)
    if not updated:
        raise HTTPException(status_code=404, detail="Event not found")
    return updated

@router.delete("/{event_id}")
def delete_existing_event(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an event."""
    if not delete_event(db, event_id, current_user.id):
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event deleted successfully"}