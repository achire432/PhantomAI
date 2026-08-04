"""
CONTEXT SCHEMAS
================
Purpose: Validate context data for API requests.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ContextUpdate(BaseModel):
    communication_style: Optional[str] = None
    response_length: Optional[str] = None
    preferred_language: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    goals: Optional[str] = None
    current_project: Optional[str] = None
    current_focus: Optional[str] = None
    active_hours_start: Optional[str] = None
    active_hours_end: Optional[str] = None
    preferred_days: Optional[str] = None

class ContextResponse(BaseModel):
    user_id: int
    communication_style: str
    response_length: str
    preferred_language: str
    full_name: Optional[str]
    role: Optional[str]
    goals: Optional[str]
    current_project: Optional[str]
    current_focus: Optional[str]
    active_hours_start: str
    active_hours_end: str
    preferred_days: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True