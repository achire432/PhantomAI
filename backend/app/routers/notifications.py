"""
NOTIFICATIONS ROUTER
=====================
Purpose: Handle notification API requests.

Endpoints:
- GET /notifications/ - Get all notifications
- GET /notifications/check - Check for due reminders
- POST /notifications/{id}/read - Mark as read

Why This Matters:
- Exposes notifications to users
- All requests require authentication
- Proactive assistant functionality
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.services.notification_service import (
    check_reminders, get_active_notifications, mark_notification_read,
    create_notification
)

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/")
def get_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all active notifications.
    """
    return {
        "notifications": get_active_notifications(db, current_user.id)
    }

@router.get("/check")
def check_for_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Check for due reminders and system alerts.
    """
    due = check_reminders(db, current_user.id)
    return {
        "due_reminders": [{
            "id": r.id,
            "title": r.title,
            "description": r.description
        } for r in due]
    }

@router.post("/{notification_id}/read")
def mark_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark a notification as read.
    """
    if not mark_notification_read(db, notification_id, current_user.id):
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"message": "Notification marked as read"}