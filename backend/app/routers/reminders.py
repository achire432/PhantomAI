"""
Purpose: Handle API requests for reminders.

Endpoints:

- POST /reminders/ - Create a reminder
- GET /reminders/ - Get all upcoming reminders
- GET /reminders/{id} - Get one reminder
- PUT /reminders/{id} - Update a reminder
- DELETE /reminders/{id} - Delete a reminder
- POST /reminders/{id}/complete - Mark as completed
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.schemas.reminder import (
    ReminderCreate,
    ReminderUpdate,
    ReminderResponse,
)
from backend.app.services.reminder_service import (
    create_reminder,
    get_reminders,
    get_reminder,
    update_reminder,
    delete_reminder,
    complete_reminder,
)

router = APIRouter(
    prefix="/reminders",
    tags=["Reminders"],
)


# ============================================================
# CREATE REMINDER
# ============================================================

@router.post(
    "/",
    response_model=ReminderResponse,
)
def create_new_reminder(
    reminder: ReminderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new reminder.
    """
    return create_reminder(
        db,
        current_user.id,
        reminder,
    )


# ============================================================
# GET REMINDERS
# ============================================================

@router.get(
    "/",
    response_model=list[ReminderResponse],
)
def list_reminders(
    upcoming: bool = True,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get reminders for the current user.

    By default, only upcoming incomplete reminders
    are returned.
    """
    return get_reminders(
        db,
        current_user.id,
        upcoming,
    )


# ============================================================
# GET ONE REMINDER
# ============================================================

@router.get(
    "/{reminder_id}",
    response_model=ReminderResponse,
)
def get_reminder_by_id(
    reminder_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get a specific reminder by ID.
    """

    reminder = get_reminder(
        db,
        reminder_id,
        current_user.id,
    )

    if not reminder:
        raise HTTPException(
            status_code=404,
            detail="Reminder not found",
        )

    return reminder


# ============================================================
# UPDATE REMINDER
# ============================================================

@router.put(
    "/{reminder_id}",
    response_model=ReminderResponse,
)
def update_existing_reminder(
    reminder_id: int,
    reminder: ReminderUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update an existing reminder.
    """

    updated = update_reminder(
        db,
        reminder_id,
        current_user.id,
        reminder,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Reminder not found",
        )

    return updated


# ============================================================
# DELETE REMINDER
# ============================================================

@router.delete(
    "/{reminder_id}",
)
def delete_existing_reminder(
    reminder_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete a reminder.
    """

    deleted = delete_reminder(
        db,
        reminder_id,
        current_user.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Reminder not found",
        )

    return {
        "message": "Reminder deleted successfully",
    }


# ============================================================
# COMPLETE REMINDER
# ============================================================

@router.post(
    "/{reminder_id}/complete",
)
def complete_existing_reminder(
    reminder_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Mark a reminder as completed.
    """

    completed = complete_reminder(
        db,
        reminder_id,
        current_user.id,
    )

    if not completed:
        raise HTTPException(
            status_code=404,
            detail="Reminder not found",
        )

    return {
        "message": "Reminder marked as completed",
    }