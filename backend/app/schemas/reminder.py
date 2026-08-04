"""
REMINDER SCHEMAS
=================
Purpose: Validate reminder data for API requests.

Why This Matters:
- Ensures data is valid before saving
- Controls what data is exposed to users
- Prevents invalid dates and times
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReminderCreate(BaseModel):
    title: str
    description: Optional[str] = None
    remind_at: datetime

class ReminderUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    remind_at: Optional[datetime] = None
    is_completed: Optional[bool] = None

class ReminderResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    remind_at: datetime
    is_completed: bool
    is_notified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True