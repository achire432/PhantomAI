"""
TASK MODEL
===========
Purpose: Store user tasks in the database.

What This File Does:
- Defines the Task table structure
- Each task has: id, user_id, title, description, priority, status, due_date, timestamps

Why We Need This:
- Users need to track to-do items
- Tasks are stored per user
- Tasks have status and priority for organization
"""

from sqlalchemy import String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from backend.app.database.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    priority: Mapped[str] = mapped_column(String(20), default="medium")  # low, medium, high
    status: Mapped[str] = mapped_column(String(20), default="pending")   # pending, in_progress, completed
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)