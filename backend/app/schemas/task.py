from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    """
    Data required when creating a task.
    """

    title: str
    description: str | None = None
    priority: str = "medium"
    due_date: datetime | None = None


class TaskUpdate(BaseModel):
    """
    Data accepted when updating a task.
    All fields are optional.
    """

    title: str | None = None
    description: str | None = None
    priority: str | None = None
    status: str | None = None
    due_date: datetime | None = None


class TaskResponse(BaseModel):
    """
    Data returned to the frontend.
    """

    id: int
    user_id: int
    title: str
    description: str | None
    priority: str
    status: str
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)