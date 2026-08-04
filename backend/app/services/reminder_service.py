"""
REMINDER SERVICE
=================
Purpose: Manage user reminders.

Why This Matters:
- Creates, reads, updates, and deletes reminders
- Checks for upcoming reminders
- Marks reminders as notified when sent

How It Works:
1. User sets a reminder with date/time
2. Reminder is stored in database
3. System checks for upcoming reminders
4. When time comes, PhantomAI notifies the user
5. User marks as completed

Which Files Use This:
- reminders.py router (API endpoints)
- (Future) Background task for checking reminders
"""

from sqlalchemy.orm import Session
from backend.app.models.reminder import Reminder
from backend.app.schemas.reminder import ReminderCreate, ReminderUpdate
from datetime import datetime

def create_reminder(db: Session, user_id: int, reminder_data: ReminderCreate) -> Reminder:
    """Create a new reminder."""
    reminder = Reminder(
        user_id=user_id,
        title=reminder_data.title,
        description=reminder_data.description,
        remind_at=reminder_data.remind_at
    )
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder

def get_reminders(db: Session, user_id: int, upcoming: bool = True) -> list:
    """
    Get reminders for a user.
    
    If upcoming=True, only get reminders that are not completed and
    have a remind_at time in the future.
    """
    query = db.query(Reminder).filter(Reminder.user_id == user_id)
    
    if upcoming:
        query = query.filter(
            Reminder.is_completed == False,
            Reminder.remind_at > datetime.utcnow()
        )
    
    return query.order_by(Reminder.remind_at).all()

def get_reminder(db: Session, reminder_id: int, user_id: int) -> Reminder:
    """Get a specific reminder by ID."""
    return db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == user_id
    ).first()

def update_reminder(db: Session, reminder_id: int, user_id: int, reminder_data: ReminderUpdate) -> Reminder:
    """Update an existing reminder."""
    reminder = get_reminder(db, reminder_id, user_id)
    if not reminder:
        return None
    
    if reminder_data.title is not None:
        reminder.title = reminder_data.title
    if reminder_data.description is not None:
        reminder.description = reminder_data.description
    if reminder_data.remind_at is not None:
        reminder.remind_at = reminder_data.remind_at
    if reminder_data.is_completed is not None:
        reminder.is_completed = reminder_data.is_completed
    
    reminder.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(reminder)
    return reminder

def delete_reminder(db: Session, reminder_id: int, user_id: int) -> bool:
    """Delete a reminder."""
    reminder = get_reminder(db, reminder_id, user_id)
    if not reminder:
        return False
    db.delete(reminder)
    db.commit()
    return True

def complete_reminder(db: Session, reminder_id: int, user_id: int) -> bool:
    """Mark a reminder as completed."""
    reminder = get_reminder(db, reminder_id, user_id)
    if not reminder:
        return False
    reminder.is_completed = True
    db.commit()
    return True