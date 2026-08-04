"""
CONTEXT ROUTER
===============
Purpose: Handle context API requests.

Endpoints:
- GET /context/ - Get user context
- PUT /context/ - Update user context
- GET /context/summary - Get context summary

Why This Matters:
- Exposes context functionality to users
- All requests require authentication
- Personalizes PhantomAI experience
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.schemas.context import ContextUpdate, ContextResponse
from backend.app.services.context_service import get_context, update_context, get_context_summary

router = APIRouter(prefix="/context", tags=["Context"])

@router.get("/", response_model=ContextResponse)
def get_user_context(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user context."""
    return get_context(db, current_user.id)

@router.put("/", response_model=ContextResponse)
def update_user_context(
    context: ContextUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user context."""
    return update_context(db, current_user.id, context)

@router.get("/summary")
def get_context_summary_endpoint(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get context summary for AI."""
    return get_context_summary(db, current_user.id)