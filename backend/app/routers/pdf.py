"""
PDF ROUTER
===========
Purpose: Generate PDF files from PhantomAI data.

Endpoints:
- GET /pdf/conversation/{id} - Generate conversation PDF
- GET /pdf/notes - Generate notes PDF
- GET /pdf/tasks - Generate tasks PDF
"""

from fastapi import APIRouter, Depends, HTTPException
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
    generate_tasks_pdf
)

router = APIRouter(prefix="/pdf", tags=["PDF"])

@router.get("/conversation/{conversation_id}")
def generate_conversation_pdf_endpoint(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate a PDF from a conversation.
    """
    # Get conversation
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Get messages
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at).all()
    
    # Build data
    conversation_data = {
        "title": conversation.title or "Conversation",
        "created_at": conversation.created_at.isoformat(),
        "messages": [{"role": m.role, "content": m.content} for m in messages]
    }
    
    # Generate PDF
    pdf_buffer = generate_conversation_pdf(conversation_data)
    
    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="conversation_{conversation_id}.pdf"'
        }
    )

@router.get("/notes")
def generate_notes_pdf_endpoint(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate a PDF from all notes.
    """
    notes = db.query(Note).filter(Note.user_id == current_user.id).all()
    
    notes_data = [{
        "title": n.title,
        "content": n.content,
        "created_at": n.created_at.isoformat()
    } for n in notes]
    
    pdf_buffer = generate_notes_pdf(notes_data)
    
    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": 'attachment; filename="notes.pdf"'
        }
    )

@router.get("/tasks")
def generate_tasks_pdf_endpoint(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate a PDF from all tasks.
    """
    tasks = db.query(Task).filter(Task.user_id == current_user.id).all()
    
    tasks_data = [{
        "title": t.title,
        "status": t.status,
        "priority": t.priority,
        "due_date": t.due_date.isoformat() if t.due_date else None
    } for t in tasks]
    
    pdf_buffer = generate_tasks_pdf(tasks_data)
    
    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": 'attachment; filename="tasks.pdf"'
        }
    )