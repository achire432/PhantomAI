"""
MEMORY SCHEMAS
===============
Purpose: Validate memory data for API requests.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MemoryCreate(BaseModel):
    key: str
    value: str
    category: Optional[str] = "general"
    importance: Optional[int] = 3
    expires_at: Optional[datetime] = None

class MemoryUpdate(BaseModel):
    value: Optional[str] = None
    importance: Optional[int] = None
    expires_at: Optional[datetime] = None

class MemoryResponse(BaseModel):
    id: int
    user_id: int
    key: str
    value: str
    category: str
    importance: int
    source: str
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime]

    class Config:
        from_attributes = True

class MemorySearchResult(BaseModel):
    key: str
    value: str
    category: str
    relevance: float