"""
TASK SCHEMAS
=============
Purpose: Validate task data for API requests.

What This File Does:
- TaskCreate: Validates data when creating a task
- TaskUpdate: Validates data when updating a task
- TaskResponse: Defines what is returned to the user

Why We Need This:
- Ensures data is valid before saving to database
- Controls what data is exposed to the user
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    due_date: Optional[datetime] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None

class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    priority: str
    status: str
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True