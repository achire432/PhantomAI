from sqlalchemy.orm import Session
from backend.app.models.settings import UserSettings
from backend.app.schemas.settings import (
    UserSettingsUpdate,
    ToolPermissionsUpdate,
)
from datetime import datetime


# ============================================================
# DEFAULT TOOL PERMISSIONS
# ============================================================

DEFAULT_TOOL_PERMISSIONS = {

    # AI / Intelligence
    "web_search": "allowed",
    "calculator": "allowed",
    "code_analysis": "allowed",
    "markdown": "allowed",

    # Files / Documents
    "file_reading": "allowed",
    "file_management": "allowed",
    "file_upload": "allowed",
    "pdf": "allowed",
    "ocr": "allowed",

    # Media
    "image_understanding": "allowed",
    "image_generation": "allowed",
    "video_generation": "allowed",

    # Productivity
    "notes": "allowed",
    "tasks": "allowed",
    "calendar": "allowed",
    "reminders": "allowed",

    # Communication
    "email_reading": "allowed",
    "email_sending": "allowed",

    # Computer / System
    "application_launcher": "allowed",
    "terminal": "allowed",
    "database": "allowed",
    "system_info": "allowed",
    "git": "allowed",

    # Memory / Context
    "memory": "allowed",
    "context": "allowed",

    # Voice
    "voice": "allowed",
    "wake_word": "allowed",

    # AI model management
    "model_management": "allowed",

    # Notifications / proactive
    "notifications": "allowed",
    "proactive": "allowed",

    # Data
    "data": "allowed",

    # Weather
    "weather": "allowed",
}


# ============================================================
# DEFAULT SETTINGS
# ============================================================

def get_default_settings() -> dict:
    return {
        "display_name": None,
        "profile_picture": None,
        "timezone": "UTC",
        "language": "en",

        "assistant_name": "PhantomAI",
        "personality": "helpful",
        "response_style": "balanced",
        "response_length": "medium",
        "proactive_mode": True,

        "ai_provider": "local",
        "ai_model": "qwen-4b",
        "fallback_provider": "groq",
        "fallback_model": "groq-llama3",
        "local_ai_enabled": True,
        "cloud_ai_enabled": True,

        "voice_enabled": True,
        "wake_word_enabled": True,
        "wake_word": "Hey Phantom",
        "auto_speak": True,
        "speech_speed": 150,
        "voice_name": "default",

        "memory_enabled": True,
        "conversation_memory_enabled": True,
        "long_term_memory_enabled": True,
        "memory_confirmation": True,

        "notifications_enabled": True,
        "task_notifications": True,
        "reminder_notifications": True,
        "system_notifications": True,
        "proactive_notifications": True,

        "theme": "dark",
        "accent_color": "#00d4ff",
        "compact_mode": False,

        "tool_permissions": DEFAULT_TOOL_PERMISSIONS.copy(),
    }


# ============================================================
# GET / CREATE SETTINGS
# ============================================================

def get_settings(db: Session, user_id: int) -> UserSettings:

    settings = (
        db.query(UserSettings)
        .filter(UserSettings.user_id == user_id)
        .first()
    )

    if not settings:
        settings = UserSettings(
            user_id=user_id,
            **get_default_settings()
        )

        db.add(settings)
        db.commit()
        db.refresh(settings)

    else:
        # ----------------------------------------------------
        # IMPORTANT:
        # Add newly introduced permissions to old users.
        # ----------------------------------------------------

        current_permissions = settings.tool_permissions or {}

        changed = False

        for tool_name, default_permission in DEFAULT_TOOL_PERMISSIONS.items():
            if tool_name not in current_permissions:
                current_permissions[tool_name] = default_permission
                changed = True

        if changed:
            settings.tool_permissions = current_permissions
            settings.updated_at = datetime.utcnow()

            db.commit()
            db.refresh(settings)

    return settings


# ============================================================
# SETTINGS -> DICTIONARY
# ============================================================

def settings_to_dict(settings: UserSettings) -> dict:

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

        "tool_permissions": settings.tool_permissions or {},

        "created_at": settings.created_at,
        "updated_at": settings.updated_at,
    }


def get_settings_dict(db: Session, user_id: int) -> dict:
    settings = get_settings(db, user_id)
    return settings_to_dict(settings)


# ============================================================
# UPDATE SETTINGS
# ============================================================

def update_settings(
    db: Session,
    user_id: int,
    update_data: UserSettingsUpdate,
) -> UserSettings:

    settings = get_settings(db, user_id)

    update_dict = update_data.model_dump(
        exclude_none=True
    )

    # --------------------------------------------------------
    # Handle tool permissions separately.
    # --------------------------------------------------------

    if "tool_permissions" in update_dict:

        permission_updates = update_dict.pop(
            "tool_permissions"
        )

        current_permissions = (
            settings.tool_permissions or {}
        ).copy()

        current_permissions.update(
            permission_updates
        )

        settings.tool_permissions = current_permissions

    # --------------------------------------------------------
    # Update normal settings.
    # --------------------------------------------------------

    for key, value in update_dict.items():

        if hasattr(settings, key):
            setattr(settings, key, value)

    settings.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(settings)

    return settings


# ============================================================
# RESET SETTINGS
# ============================================================

def reset_settings(
    db: Session,
    user_id: int,
) -> UserSettings:

    settings = get_settings(db, user_id)

    defaults = get_default_settings()

    for key, value in defaults.items():

        if hasattr(settings, key):

            if key == "tool_permissions":
                setattr(
                    settings,
                    key,
                    value.copy()
                )
            else:
                setattr(
                    settings,
                    key,
                    value
                )

    settings.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(settings)

    return settings


# ============================================================
# SINGLE SETTING
# ============================================================

def get_setting(
    db: Session,
    user_id: int,
    key: str,
):
    settings = get_settings(db, user_id)

    return getattr(settings, key, None)


# ============================================================
# TOOL PERMISSION HELPERS
# ============================================================

def get_tool_permission(
    db: Session,
    user_id: int,
    tool_name: str,
) -> str:

    settings = get_settings(db, user_id)

    permissions = settings.tool_permissions or {}

    return permissions.get(
        tool_name,
        "disabled",
    )


def is_tool_allowed(
    db: Session,
    user_id: int,
    tool_name: str,
) -> bool:

    return (
        get_tool_permission(
            db,
            user_id,
            tool_name,
        )
        == "allowed"
    )


def needs_confirmation(
    db: Session,
    user_id: int,
    tool_name: str,
) -> bool:

    return (
        get_tool_permission(
            db,
            user_id,
            tool_name,
        )
        == "confirmation_required"
    )


def is_tool_disabled(
    db: Session,
    user_id: int,
    tool_name: str,
) -> bool:

    return (
        get_tool_permission(
            db,
            user_id,
            tool_name,
        )
        == "disabled"
    )


# ============================================================
# AI SETTINGS
# ============================================================

def get_active_model(
    db: Session,
    user_id: int,
) -> str:

    settings = get_settings(db, user_id)

    return settings.ai_model


def get_response_style(
    db: Session,
    user_id: int,
) -> str:

    settings = get_settings(db, user_id)

    return settings.response_style


# ============================================================
# VOICE
# ============================================================

def is_voice_enabled(
    db: Session,
    user_id: int,
) -> bool:

    settings = get_settings(db, user_id)

    return settings.voice_enabled


# ============================================================
# MEMORY
# ============================================================

def is_memory_enabled(
    db: Session,
    user_id: int,
) -> bool:

    settings = get_settings(db, user_id)

    return settings.memory_enabled
