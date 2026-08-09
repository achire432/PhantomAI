from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator


class CalendarEventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: datetime
    end_time: datetime
    all_day: bool = False

    @model_validator(mode="after")
    def validate_times(self):
        if self.end_time <= self.start_time:
            raise ValueError("End time must be after start time.")
        return self


class CalendarEventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    all_day: Optional[bool] = None


class CalendarEventResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    location: Optional[str]
    start_time: datetime
    end_time: datetime
    all_day: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True