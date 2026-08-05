"""
SETTINGS SERVICE
=================
Purpose: Central management of user settings.

Why This Matters:
- One source of truth for all settings
- Other parts of PhantomAI use this service
- Tool permission checks are centralized
- Default settings are created automatically

How It Works:
1. When a user requests settings, we check if they exist
2. If not, we create them with defaults
3. Users can update individual settings
4. Tools check permissions through this service

What Would Happen Without This:
- Settings logic would be scattered everywhere
- No consistent way to check permissions
- No default settings for new users

Which Files Use This:
- routers/settings.py (API endpoints)
- routers/*.py (tools check permissions here)
- ai.py (for response style)
- voice.py (for voice settings)
"""

from sqlalchemy.orm import Session
from backend.app.models.settings import UserSettings
from backend.app.models.user import User
from backend.app.schemas.settings import UserSettingsUpdate, ToolPermissions
from datetime import datetime
import json


# ============================================
# DEFAULT SETTINGS
# ============================================

DEFAULT_TOOL_PERMISSIONS = {
    "web_search": "allowed",
    "file_reading": "allowed",
    "file_management": "confirmation_required",
    "email_reading": "allowed",
    "email_sending": "confirmation_required",
    "terminal": "disabled",
    "database": "confirmation_required",
    "application_launcher": "allowed",
    "calendar": "allowed",
    "memory": "allowed",
    "git": "allowed",
    "system_info": "allowed",
    "weather": "allowed",
    "ocr": "allowed",
    "image_generation": "allowed",
    "video_generation": "allowed",
    "calculator": "allowed",
    "notes": "allowed",
    "tasks": "allowed",
    "reminders": "allowed"
}


def get_default_settings() -> dict:
    """Return default settings for a new user."""
    return {
        # Profile
        "display_name": None,
        "profile_picture": None,
        "timezone": "UTC",
        "language": "en",
        
        # PhantomAI Behaviour
        "assistant_name": "PhantomAI",
        "personality": "helpful",
        "response_style": "balanced",
        "response_length": "medium",
        "proactive_mode": True,
        
        # AI
        "ai_provider": "local",
        "ai_model": "qwen-4b",
        "fallback_provider": "groq",
        "fallback_model": "groq-llama3",
        "local_ai_enabled": True,
        "cloud_ai_enabled": True,
        
        # Voice
        "voice_enabled": True,
        "wake_word_enabled": True,
        "wake_word": "Hey Phantom",
        "auto_speak": True,
        "speech_speed": 150,
        "voice_name": "default",
        
        # Memory
        "memory_enabled": True,
        "conversation_memory_enabled": True,
        "long_term_memory_enabled": True,
        "memory_confirmation": True,
        
        # Notifications
        "notifications_enabled": True,
        "task_notifications": True,
        "reminder_notifications": True,
        "system_notifications": True,
        "proactive_notifications": True,
        
        # Appearance
        "theme": "dark",
        "accent_color": "#00d4ff",
        "compact_mode": False,
        
        # Tool Permissions
        "tool_permissions": DEFAULT_TOOL_PERMISSIONS
    }


def get_settings(db: Session, user_id: int) -> UserSettings:
    """
    Get or create settings for a user.
    
    How It Works:
    1. Checks if settings exist in the database
    2. If yes, returns them
    3. If no, creates default settings and returns them
    
    Why This Matters:
    - Every user needs settings
    - New users get sensible defaults
    - Prevents "settings not found" errors
    """
    settings = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
    
    if not settings:
        # Create default settings
        defaults = get_default_settings()
        
        settings = UserSettings(
            user_id=user_id,
            **defaults
        )
        db.add(settings)
        db.commit()
        db.refresh(settings)
    
    return settings


def get_settings_dict(db: Session, user_id: int) -> dict:
    """Get settings as a dictionary (for API responses)."""
    settings = get_settings(db, user_id)
    return settings_to_dict(settings)


def settings_to_dict(settings: UserSettings) -> dict:
    """Convert a UserSettings object to a dictionary."""
    return {
        "display_name": settings.display_name,
        "profile_picture": settings.profile_picture,
        "timezone": settings.timezone,
        "language": settings.language,
        "assistant_name": settings.assistant_name,
        "personality": settings.personality,
        "response_style": settings.response_style,
        "response_length": settings.response_length,
        "proactive_mode": settings.proactive_mode,
        "ai_provider": settings.ai_provider,
        "ai_model": settings.ai_model,
        "fallback_provider": settings.fallback_provider,
        "fallback_model": settings.fallback_model,
        "local_ai_enabled": settings.local_ai_enabled,
        "cloud_ai_enabled": settings.cloud_ai_enabled,
        "voice_enabled": settings.voice_enabled,
        "wake_word_enabled": settings.wake_word_enabled,
        "wake_word": settings.wake_word,
        "auto_speak": settings.auto_speak,
        "speech_speed": settings.speech_speed,
        "voice_name": settings.voice_name,
        "memory_enabled": settings.memory_enabled,
        "conversation_memory_enabled": settings.conversation_memory_enabled,
        "long_term_memory_enabled": settings.long_term_memory_enabled,
        "memory_confirmation": settings.memory_confirmation,
        "notifications_enabled": settings.notifications_enabled,
        "task_notifications": settings.task_notifications,
        "reminder_notifications": settings.reminder_notifications,
        "system_notifications": settings.system_notifications,
        "proactive_notifications": settings.proactive_notifications,
        "theme": settings.theme,
        "accent_color": settings.accent_color,
        "compact_mode": settings.compact_mode,
        "tool_permissions": settings.tool_permissions,
        "created_at": settings.created_at,
        "updated_at": settings.updated_at
    }


def update_settings(db: Session, user_id: int, update_data: UserSettingsUpdate) -> UserSettings:
    """
    Update settings for a user.
    
    How It Works:
    1. Gets the user's settings
    2. Updates only the fields that were provided
    3. Saves to the database
    4. Returns the updated settings
    
    Why This Matters:
    - Users can customize PhantomAI
    - Partial updates are supported
    - Invalid fields are ignored
    """
    settings = get_settings(db, user_id)
    update_dict = update_data.dict(exclude_none=True)
    
    # Handle tool_permissions separately (it's a nested object)
    if "tool_permissions" in update_dict:
        tool_perms = update_dict["tool_permissions"]
        if isinstance(tool_perms, dict):
            # Merge with existing permissions
            current_perms = settings.tool_permissions or {}
            current_perms.update(tool_perms)
            settings.tool_permissions = current_perms
        elif isinstance(tool_perms, ToolPermissions):
            settings.tool_permissions = tool_perms.dict()
        del update_dict["tool_permissions"]
    
    # Update all other fields
    for key, value in update_dict.items():
        if hasattr(settings, key):
            setattr(settings, key, value)
    
    # Update timestamp
    settings.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(settings)
    return settings


def reset_settings(db: Session, user_id: int) -> UserSettings:
    """
    Reset settings to defaults.
    
    How It Works:
    1. Gets the user's settings
    2. Overwrites with default values
    3. Saves to the database
    
    Why This Matters:
    - Users can revert to defaults
    - Undo accidental changes
    - Fresh start
    """
    settings = get_settings(db, user_id)
    defaults = get_default_settings()
    
    for key, value in defaults.items():
        if hasattr(settings, key):
            setattr(settings, key, value)
    
    settings.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(settings)
    return settings


def get_setting(db: Session, user_id: int, key: str):
    """Get a single setting value."""
    settings = get_settings(db, user_id)
    return getattr(settings, key, None)


def is_tool_allowed(db: Session, user_id: int, tool_name: str) -> bool:
    """
    Check if a tool is allowed for a user.
    
    How It Works:
    1. Gets the user's settings
    2. Checks the tool permission
    3. Returns True if 'allowed', False otherwise
    
    Why This Matters:
    - Tools can check permissions before running
    - Users control which tools are allowed
    - Security is centralized
    
    Permission Levels:
    - "allowed": The tool can run freely
    - "confirmation_required": Must ask user first
    - "disabled": Cannot run at all
    """
    settings = get_settings(db, user_id)
    permissions = settings.tool_permissions or {}
    permission = permissions.get(tool_name, "disabled")
    return permission == "allowed"


def needs_confirmation(db: Session, user_id: int, tool_name: str) -> bool:
    """
    Check if a tool needs user confirmation.
    
    Returns:
    - True if the tool requires confirmation
    - False if it's allowed or disabled
    """
    settings = get_settings(db, user_id)
    permissions = settings.tool_permissions or {}
    permission = permissions.get(tool_name, "disabled")
    return permission == "confirmation_required"


def is_tool_disabled(db: Session, user_id: int, tool_name: str) -> bool:
    """Check if a tool is disabled for a user."""
    settings = get_settings(db, user_id)
    permissions = settings.tool_permissions or {}
    permission = permissions.get(tool_name, "disabled")
    return permission == "disabled"


def get_active_model(db: Session, user_id: int) -> str:
    """
    Get the active AI model for a user.
    
    Why This Matters:
    - Users can choose which AI model they prefer
    - Settings store the user's preference
    - The AI system uses this to route requests
    """
    settings = get_settings(db, user_id)
    return settings.ai_model


def get_response_style(db: Session, user_id: int) -> str:
    """Get the user's preferred response style."""
    settings = get_settings(db, user_id)
    return settings.response_style


def is_voice_enabled(db: Session, user_id: int) -> bool:
    """Check if voice is enabled for a user."""
    settings = get_settings(db, user_id)
    return settings.voice_enabled


def is_memory_enabled(db: Session, user_id: int) -> bool:
    """Check if memory is enabled for a user."""
    settings = get_settings(db, user_id)
    return settings.memory_enabled