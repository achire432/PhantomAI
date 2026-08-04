"""
MEMORY MODEL
=============
Purpose: Store long-term memory entries for PhantomAI.

Why This Matters:
- PhantomAI remembers important facts
- Creates a personalized experience
- Builds a knowledge graph of your life

What It Stores:
- Facts (key-value pairs)
- Preferences
- Projects
- Important dates
- Relationships between information

How It Works:
- Each memory belongs to a user
- Can be searched and retrieved
- Important memories are prioritized
"""

from sqlalchemy import String, Integer, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from backend.app.database.database import Base

class Memory(Base):
    __tablename__ = "memories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Memory content
    key: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Memory metadata
    category: Mapped[str] = mapped_column(String(50), default="general")  # fact, preference, project, date, goal
    importance: Mapped[int] = mapped_column(Integer, default=3)  # 1-10 (higher = more important)
    source: Mapped[str] = mapped_column(String(50), default="user")  # user, ai, system
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)  # Optional expiration