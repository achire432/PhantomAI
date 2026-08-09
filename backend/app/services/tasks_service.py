from datetime import datetime

from sqlalchemy.orm import Session

from backend.app.models.task import Task
from backend.app.schemas.task import TaskCreate, TaskUpdate


def create_task(
    db: Session,
    user_id: int,
    task_data: TaskCreate
) -> Task:
    """
    Create and save a new task.
    """

    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority or "medium",
        due_date=task_data.due_date,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_tasks(
    db: Session,
    user_id: int,
    status: str | None = None
) -> list[Task]:
    """
    Get all tasks belonging to the current user.

    If status is provided, only tasks with that status
    are returned.
    """

    query = db.query(Task).filter(
        Task.user_id == user_id
    )

    if status:
        query = query.filter(
            Task.status == status
        )

    return query.order_by(
        Task.due_date.asc().nullslast(),
        Task.created_at.desc()
    ).all()


def get_task(
    db: Session,
    task_id: int,
    user_id: int
) -> Task | None:
    """
    Get one task belonging to the current user.
    """

    return db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()


def update_task(
    db: Session,
    task_id: int,
    user_id: int,
    task_data: TaskUpdate
) -> Task | None:
    """
    Update an existing task.
    """

    task = get_task(
        db,
        task_id,
        user_id
    )

    if not task:
        return None

    if task_data.title is not None:
        task.title = task_data.title

    if task_data.description is not None:
        task.description = task_data.description

    if task_data.priority is not None:
        task.priority = task_data.priority

    if task_data.status is not None:
        task.status = task_data.status

    if task_data.due_date is not None:
        task.due_date = task_data.due_date

    task.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(task)

    return task


def delete_task(
    db: Session,
    task_id: int,
    user_id: int
) -> bool:
    """
    Delete a task belonging to the current user.
    """

    task = get_task(
        db,
        task_id,
        user_id
    )

    if not task:
        return False

    db.delete(task)
    db.commit()

    return True