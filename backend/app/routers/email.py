"""
EMAIL ROUTER
=============
Purpose: Handle email API requests.

Endpoints:
- GET /email/recent - Get recent emails
- GET /email/{id}/summarize - Summarize an email
- POST /email/draft - Create a draft reply
- POST /email/send - Send an email
- GET /email/drafts - Get all drafts
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.models.email import Email
from backend.app.schemas.email import (
    EmailResponse, 
    EmailSummaryResponse,
    EmailDraftCreate, 
    EmailDraftResponse,
    EmailSendRequest
)
from backend.app.services.email_service import (
    fetch_recent_emails, send_email, get_drafts
)
from backend.app.services.ai import ask_ai

# ============================================
# REQUEST MODELS
# ============================================

class EmailSendRequest(BaseModel):
    to: str
    subject: str
    body: str

router = APIRouter(prefix="/email", tags=["Email"])

@router.get("/recent", response_model=list[EmailResponse])
def get_recent_emails(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get recent emails for the current user."""
    result = fetch_recent_emails(db, current_user.id, limit)
    if isinstance(result, dict) and result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/{email_id}/summarize", response_model=dict)
def summarize_email(
    email_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Summarize an email using AI."""
    email = db.query(Email).filter(
        Email.id == email_id,
        Email.user_id == current_user.id
    ).first()
    
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    # Use AI to summarize
    prompt = f"Summarize this email in 2-3 sentences:\n\nFrom: {email.sender}\nSubject: {email.subject}\nBody: {email.body[:1000]}"
    summary = ask_ai(prompt)
    
    # Save summary to database
    email.summary = summary
    email.is_read = True
    db.commit()
    
    return {
        "id": email.id,
        "sender": email.sender,
        "subject": email.subject,
        "summary": summary
    }

@router.post("/draft", response_model=EmailDraftResponse)
def create_draft(
    draft: EmailDraftCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a draft email using AI."""
    prompt = f"Write a professional email to {draft.to} about {draft.subject}\n\n{draft.body}\n\nWrite a clear, professional email."
    body = ask_ai(
    prompt,
    mode="email_draft"
)
    
    return {
        "id": 1,
        "to": draft.to,
        "subject": draft.subject,
        "body": body,
        "is_sent": False,
        "created_at": datetime.now()
    }

@router.post("/send")
def send_email_request(
    email_data: EmailSendRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send an email."""
    result = send_email(db, current_user.id, email_data.to, email_data.subject, email_data.body)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result

@router.get("/drafts")
def get_draft_emails(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all drafts for the current user."""
    return get_drafts(db, current_user.id)