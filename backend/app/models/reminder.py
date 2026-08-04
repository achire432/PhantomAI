"""
REMINDER MODEL
===============
Purpose: Store user reminders in the database.

Why This Matters:
- Users need to remember tasks and events
- PhantomAI can proactively remind users
- Creates a reliable assistant experience

What Would Happen Without This:
- Users would forget important tasks
- PhantomAI couldn't be proactive
- Limited to reactive responses only

Which Files Use This:
- reminder_service.py (to manage reminders)
- reminders.py router (API endpoints)
"""

from sqlalchemy import String, Integer, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from backend.app.database.database import Base

class Reminder(Base):
    __tablename__ = "reminders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    remind_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    is_notified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)