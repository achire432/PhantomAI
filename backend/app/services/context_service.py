"""
CONTEXT SERVICE
=================
Purpose: Manage user context data.

Why This Matters:
- Stores user preferences
- Tracks active projects
- Learns user behavior

How It Works:
1. User provides context (preferences, projects)
2. PhantomAI stores it
3. PhantomAI uses it to personalize responses
"""

from sqlalchemy.orm import Session
from backend.app.models.context import UserContext
from backend.app.schemas.context import ContextUpdate
from datetime import datetime

def get_context(db: Session, user_id: int) -> UserContext:
    """Get user context."""
    context = db.query(UserContext).filter(UserContext.user_id == user_id).first()
    if not context:
        # Create default context if none exists
        context = UserContext(user_id=user_id)
        db.add(context)
        db.commit()
        db.refresh(context)
    return context

def update_context(db: Session, user_id: int, context_data: ContextUpdate) -> UserContext:
    """Update user context."""
    context = get_context(db, user_id)
    
    if context_data.communication_style is not None:
        context.communication_style = context_data.communication_style
    if context_data.response_length is not None:
        context.response_length = context_data.response_length
    if context_data.preferred_language is not None:
        context.preferred_language = context_data.preferred_language
    if context_data.full_name is not None:
        context.full_name = context_data.full_name
    if context_data.role is not None:
        context.role = context_data.role
    if context_data.goals is not None:
        context.goals = context_data.goals
    if context_data.current_project is not None:
        context.current_project = context_data.current_project
    if context_data.current_focus is not None:
        context.current_focus = context_data.current_focus
    if context_data.active_hours_start is not None:
        context.active_hours_start = context_data.active_hours_start
    if context_data.active_hours_end is not None:
        context.active_hours_end = context_data.active_hours_end
    if context_data.preferred_days is not None:
        context.preferred_days = context_data.preferred_days
    
    context.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(context)
    return context

def get_context_summary(db: Session, user_id: int) -> dict:
    """Get a summary of user context for AI prompts."""
    context = get_context(db, user_id)
    
    return {
        "communication_style": context.communication_style,
        "response_length": context.response_length,
        "full_name": context.full_name,
        "role": context.role,
        "goals": context.goals,
        "current_project": context.current_project,
        "current_focus": context.current_focus,
        "active_hours": f"{context.active_hours_start} - {context.active_hours_end}",
        "preferred_days": context.preferred_days
    }