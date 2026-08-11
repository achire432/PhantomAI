"""
PDF ROUTER

Purpose:
Generate PDF files from PhantomAI data.

Endpoints:
- GET /pdf/conversation/{id} - Generate conversation PDF
- GET /pdf/notes - Generate all or selected notes PDF
- GET /pdf/tasks - Generate all or selected tasks PDF
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.models.conversation import Conversation
from backend.app.models.message import Message
from backend.app.models.note import Note
from backend.app.models.task import Task
from backend.app.services.pdf_service import (
    generate_conversation_pdf,
    generate_notes_pdf,
    generate_tasks_pdf,
)

router = APIRouter(prefix="/pdf", tags=["PDF"])


# ============================================================
# CONVERSATION PDF
# ============================================================

@router.get("/conversation/{conversation_id}")
def generate_conversation_pdf_endpoint(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Generate a PDF from a conversation.
    """

    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id,
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at).all()

    conversation_data = {
        "title": conversation.title or "Conversation",
        "created_at": conversation.created_at.isoformat(),
        "messages": [
            {
                "role": m.role,
                "content": m.content,
            }
            for m in messages
        ],
    }

    pdf_buffer = generate_conversation_pdf(conversation_data)

    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'attachment; filename="conversation_{conversation_id}.pdf"'
            )
        },
    )


# ============================================================
# NOTES PDF
# ============================================================

@router.get("/notes")
def generate_notes_pdf_endpoint(
    ids: str | None = Query(
        default=None,
        description="Comma-separated note IDs. Omit to export all notes.",
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Generate a PDF from all notes or selected notes.

    Examples:

    /pdf/notes
        -> Export all notes

    /pdf/notes?ids=1
        -> Export note 1

    /pdf/notes?ids=1,3,5
        -> Export notes 1, 3 and 5
    """

    # --------------------------------------------------------
    # Export ALL notes
    # --------------------------------------------------------

    if not ids:
        notes = db.query(Note).filter(
            Note.user_id == current_user.id
        ).all()

    # --------------------------------------------------------
    # Export SELECTED notes
    # --------------------------------------------------------

    else:
        try:
            note_ids = [
                int(note_id.strip())
                for note_id in ids.split(",")
                if note_id.strip()
            ]
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid note ID. IDs must be numbers.",
            )

        if not note_ids:
            raise HTTPException(
                status_code=400,
                detail="No valid note IDs provided.",
            )

        notes = db.query(Note).filter(
            Note.user_id == current_user.id,
            Note.id.in_(note_ids),
        ).all()

        # Prevent exporting IDs that do not belong to this user
        found_ids = {note.id for note in notes}
        missing_ids = set(note_ids) - found_ids

        if missing_ids:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"Note(s) not found: "
                    f"{', '.join(map(str, sorted(missing_ids)))}"
                ),
            )

    notes_data = [
        {
            "title": note.title,
            "content": note.content,
            "created_at": (
                note.created_at.isoformat()
                if note.created_at
                else None
            ),
        }
        for note in notes
    ]

    pdf_buffer = generate_notes_pdf(notes_data)

    filename = "notes.pdf" if not ids else "selected_notes.pdf"

    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )


# ============================================================
# TASKS PDF
# ============================================================

@router.get("/tasks")
def generate_tasks_pdf_endpoint(
    ids: str | None = Query(
        default=None,
        description="Comma-separated task IDs. Omit to export all tasks.",
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Generate a PDF from all tasks or selected tasks.

    Examples:

    /pdf/tasks
        -> Export all tasks

    /pdf/tasks?ids=1
        -> Export task 1

    /pdf/tasks?ids=1,3,5
        -> Export tasks 1, 3 and 5
    """

    # --------------------------------------------------------
    # Export ALL tasks
    # --------------------------------------------------------

    if not ids:
        tasks = db.query(Task).filter(
            Task.user_id == current_user.id
        ).all()

    # --------------------------------------------------------
    # Export SELECTED tasks
    # --------------------------------------------------------

    else:
        try:
            task_ids = [
                int(task_id.strip())
                for task_id in ids.split(",")
                if task_id.strip()
            ]
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid task ID. IDs must be numbers.",
            )

        if not task_ids:
            raise HTTPException(
                status_code=400,
                detail="No valid task IDs provided.",
            )

        tasks = db.query(Task).filter(
            Task.user_id == current_user.id,
            Task.id.in_(task_ids),
        ).all()

        # Prevent exporting IDs that do not belong to this user
        found_ids = {task.id for task in tasks}
        missing_ids = set(task_ids) - found_ids

        if missing_ids:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"Task(s) not found: "
                    f"{', '.join(map(str, sorted(missing_ids)))}"
                ),
            )

    tasks_data = [
        {
            "title": task.title,
            "status": task.status,
            "priority": task.priority,
            "due_date": (
                task.due_date.isoformat()
                if task.due_date
                else None
            ),
        }
        for task in tasks
    ]

    pdf_buffer = generate_tasks_pdf(tasks_data)

    filename = "tasks.pdf" if not ids else "selected_tasks.pdf"

    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )
