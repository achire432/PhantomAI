"""
EMAIL SCHEMAS
==============
Purpose: Validate email data for API requests.

Why This Matters:
- Ensures data is valid before processing
- Controls what data is exposed to users
- Prevents invalid data from reaching the database
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class EmailResponse(BaseModel):
    id: int
    sender: str
    subject: str
    body: str
    summary: Optional[str]
    received_at: datetime
    is_read: bool

    class Config:
        from_attributes = True

class EmailSummaryResponse(BaseModel):
    id: int
    sender: str
    subject: str
    summary: str
    received_at: datetime

class EmailDraftCreate(BaseModel):
    to: str
    subject: str
    body: str

class EmailDraftResponse(BaseModel):
    id: int
    to: str
    subject: str
    body: str
    is_sent: bool
    created_at: datetime

    class Config:
        from_attributes = True

class EmailSendRequest(BaseModel):
    to: str
    subject: str
    body: str