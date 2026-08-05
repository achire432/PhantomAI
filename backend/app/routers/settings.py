"""
SETTINGS ROUTER
================
Purpose: Handle user settings API requests.

Endpoints:
- GET /settings/ - Get user settings
- PUT /settings/ - Update user settings
- POST /settings/reset - Reset settings to defaults

Why This Matters:
- Exposes settings to users
- All requests require authentication
- Users can only access their own settings
- Central location for settings management

Security:
- JWT authentication required
- User ID is extracted from the token
- Cannot access other users' settings
- Sensitive data is never exposed
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.schemas.settings import UserSettingsResponse, UserSettingsUpdate
from backend.app.services.settings_service import (
    get_settings_dict,
    update_settings,
    reset_settings
)

router = APIRouter(prefix="/settings", tags=["Settings"])


@router.get("/", response_model=UserSettingsResponse)
def get_user_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all settings for the current user.
    
    How It Works:
    1. Authenticates the user (JWT token)
    2. Fetches or creates settings for the user
    3. Returns all settings as JSON
    
    Security:
    - Only the authenticated user can access their settings
    - No sensitive data (API keys) are exposed
    """
    return get_settings_dict(db, current_user.id)


@router.put("/", response_model=UserSettingsResponse)
def update_user_settings(
    settings_update: UserSettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user settings.
    
    How It Works:
    1. Authenticates the user
    2. Validates the input data
    3. Updates only the provided fields
    4. Saves to the database
    
    Example:
        PUT /settings
        {"response_style": "concise", "theme": "light"}
    """
    try:
        updated = update_settings(db, current_user.id, settings_update)
        return get_settings_dict(db, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/reset", response_model=UserSettingsResponse)
def reset_user_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Reset all settings to default values.
    
    How It Works:
    1. Authenticates the user
    2. Overwrites all settings with defaults
    3. Saves to the database
    
    Warning:
    - This cannot be undone
    - All customizations will be lost
    """
    try:
        reset_settings(db, current_user.id)
        return get_settings_dict(db, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tool/{tool_name}")
def check_tool_permission(
    tool_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Check if a tool is allowed for the current user.
    
    How It Works:
    1. Authenticates the user
    2. Checks the tool permission in settings
    3. Returns the permission level
    
    Permission Levels:
    - "allowed": The tool can run freely
    - "confirmation_required": Must ask the user first
    - "disabled": Cannot run at all
    
    This is used by tools to check permissions before running.
    """
    from backend.app.services.settings_service import (
        is_tool_allowed, needs_confirmation, is_tool_disabled
    )
    
    return {
        "tool": tool_name,
        "allowed": is_tool_allowed(db, current_user.id, tool_name),
        "needs_confirmation": needs_confirmation(db, current_user.id, tool_name),
        "disabled": is_tool_disabled(db, current_user.id, tool_name)
    }


@router.get("/active-model")
def get_active_model(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get the user's active AI model."""
    from backend.app.services.settings_service import get_active_model
    
    return {
        "model": get_active_model(db, current_user.id)
    }