from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.schemas.task import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)
from backend.app.services.tasks_service import (
    create_task,
    delete_task,
    get_task,
    get_tasks,
    update_task,
)


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post(
    "/",
    response_model=TaskResponse,
)
def create_new_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new task for the current user.
    """

    return create_task(
        db,
        current_user.id,
        task,
    )


@router.get(
    "/",
    response_model=list[TaskResponse],
)
def list_tasks(
    status: str | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get tasks belonging to the current user.
    """

    return get_tasks(
        db,
        current_user.id,
        status,
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
def get_task_by_id(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get one task.
    """

    task = get_task(
        db,
        task_id,
        current_user.id,
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
)
def update_existing_task(
    task_id: int,
    task: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update an existing task.
    """

    updated = update_task(
        db,
        task_id,
        current_user.id,
        task,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return updated


@router.delete(
    "/{task_id}",
)
def delete_existing_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete an existing task.
    """

    deleted = delete_task(
        db,
        task_id,
        current_user.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return {
        "message": "Task deleted successfully"
    }