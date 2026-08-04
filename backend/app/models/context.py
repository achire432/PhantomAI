"""
CONTEXT MODEL
===============
Purpose: Store user context data for PhantomAI.

Why This Matters:
- PhantomAI needs to understand who you are
- It learns your preferences over time
- This creates a personalized experience

What It Stores:
- User preferences (communication style, response length)
- Active projects (what you're working on)
- Important facts (your role, your goals)
- Behavior patterns (when you're active, how you work)

What Would Happen Without This:
- PhantomAI would treat every user the same
- No personalization
- Less helpful
"""

from sqlalchemy import String, Integer, DateTime, Text, ForeignKey, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from backend.app.database.database import Base

class UserContext(Base):
    __tablename__ = "user_context"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    
    # User Preferences
    communication_style: Mapped[str] = mapped_column(String(50), default="professional")  # professional, casual, concise, detailed
    response_length: Mapped[str] = mapped_column(String(20), default="medium")  # short, medium, long
    preferred_language: Mapped[str] = mapped_column(String(20), default="en")  # en, es, fr, etc.
    
    # User Information
    full_name: Mapped[str] = mapped_column(String(100), nullable=True)
    role: Mapped[str] = mapped_column(String(100), nullable=True)  # developer, student, designer, etc.
    goals: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Active Context
    current_project: Mapped[str] = mapped_column(String(200), nullable=True)
    current_focus: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Behavior Patterns
    active_hours_start: Mapped[str] = mapped_column(String(10), default="09:00")  # 24hr format
    active_hours_end: Mapped[str] = mapped_column(String(10), default="18:00")
    preferred_days: Mapped[str] = mapped_column(String(100), default="Monday,Tuesday,Wednesday,Thursday,Friday")  # comma-separated
    
    # Internal
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)