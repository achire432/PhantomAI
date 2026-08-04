"""
NOTIFICATION SERVICE
=====================
Purpose: Send notifications to the user.

Why This Matters:
- PhantomAI can alert you proactively
- Makes it feel like a real assistant
- Never miss important events

How It Works:
1. Creates notifications in the database
2. Checks for due reminders
3. Sends desktop notifications
4. System alerts for high CPU/RAM

What Would Happen Without This:
- You'd miss reminders
- No proactive alerts
- PhantomAI would be passive
"""

from sqlalchemy.orm import Session
from datetime import datetime
from backend.app.models.reminder import Reminder
from backend.app.models.user import User
import threading

def create_notification(db: Session, user_id: int, title: str, message: str) -> dict:
    """
    Create a notification in the database.
    """
    try:
        # We'll use the reminder model to store notifications too
        reminder = Reminder(
            user_id=user_id,
            title=title,
            description=message,
            remind_at=datetime.utcnow()
        )
        db.add(reminder)
        db.commit()
        db.refresh(reminder)
        
        return {
            "success": True,
            "id": reminder.id,
            "title": title,
            "message": message,
            "created_at": reminder.created_at
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def check_reminders(db: Session, user_id: int) -> list:
    """
    Check for due reminders.
    
    Returns:
    [
        {"id": 1, "title": "Call John", "description": "Discuss project"},
        ...
    ]
    """
    now = datetime.utcnow()
    due_reminders = db.query(Reminder).filter(
        Reminder.user_id == user_id,
        Reminder.is_completed == False,
        Reminder.is_notified == False,
        Reminder.remind_at <= now
    ).all()
    
    # Mark them as notified
    for reminder in due_reminders:
        reminder.is_notified = True
    db.commit()
    
    return due_reminders

def get_active_notifications(db: Session, user_id: int) -> list:
    """
    Get all active notifications for a user.
    """
    reminders = db.query(Reminder).filter(
        Reminder.user_id == user_id,
        Reminder.is_completed == False
    ).order_by(Reminder.remind_at).all()
    
    return [{
        "id": r.id,
        "title": r.title,
        "message": r.description,
        "time": r.remind_at.isoformat()
    } for r in reminders]

def mark_notification_read(db: Session, notification_id: int, user_id: int) -> bool:
    """
    Mark a notification as read (completed).
    """
    reminder = db.query(Reminder).filter(
        Reminder.id == notification_id,
        Reminder.user_id == user_id
    ).first()
    
    if not reminder:
        return False
    
    reminder.is_completed = True
    db.commit()
    return True