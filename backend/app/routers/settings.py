from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user

from backend.app.models.user import User
from backend.app.models.settings import UserSettings

from backend.app.schemas.settings import (
    UserSettingsResponse,
    UserSettingsUpdate,
    ToolPermissions,
    ToolPermission,
)

from backend.app.services.permission_service import PermissionService


router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
)


# ============================================================
# HELPERS
# ============================================================

def get_or_create_settings(
    db: Session,
    user: User,
) -> UserSettings:

    settings = (
        db.query(UserSettings)
        .filter(UserSettings.user_id == user.id)
        .first()
    )

    if settings:
        return settings

    settings = UserSettings(
        user_id=user.id,
        tool_permissions=PermissionService.DEFAULT_PERMISSIONS.copy(),
    )

    db.add(settings)
    db.commit()
    db.refresh(settings)

    return settings


def settings_to_response(
    settings: UserSettings,
) -> dict:

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
        "conversation_memory_enabled": (
            settings.conversation_memory_enabled
        ),
        "long_term_memory_enabled": (
            settings.long_term_memory_enabled
        ),
        "memory_confirmation": settings.memory_confirmation,

        "notifications_enabled": settings.notifications_enabled,
        "task_notifications": settings.task_notifications,
        "reminder_notifications": settings.reminder_notifications,
        "system_notifications": settings.system_notifications,
        "proactive_notifications": (
            settings.proactive_notifications
        ),

        "theme": settings.theme,
        "accent_color": settings.accent_color,
        "compact_mode": settings.compact_mode,

        "tool_permissions": PermissionService.get_permissions(
            settings
        ),

        "created_at": settings.created_at,
        "updated_at": settings.updated_at,
    }


# ============================================================
# GENERAL SETTINGS
# ============================================================

@router.get(
    "/",
    response_model=UserSettingsResponse,
)
def get_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    settings = get_or_create_settings(
        db,
        current_user,
    )

    return settings_to_response(settings)


@router.put(
    "/",
    response_model=UserSettingsResponse,
)
def update_settings(
    data: UserSettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    settings = get_or_create_settings(
        db,
        current_user,
    )

    update_data = data.model_dump(
        exclude_unset=True
    )

    # Tool permissions are handled separately so we
    # can validate them centrally.
    tool_permissions = update_data.pop(
        "tool_permissions",
        None,
    )

    for field, value in update_data.items():

        if hasattr(settings, field):
            setattr(
                settings,
                field,
                value,
            )

    if tool_permissions is not None:

        permissions = (
            tool_permissions.model_dump()
            if hasattr(
                tool_permissions,
                "model_dump",
            )
            else tool_permissions
        )

        current_permissions = (
            PermissionService.get_permissions(
                settings
            )
        )

        for tool_name, level in permissions.items():

            if tool_name not in current_permissions:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Unknown tool: {tool_name}",
                )

            PermissionService.validate_level(
                level
            )

            current_permissions[
                tool_name
            ] = level

        settings.tool_permissions = (
            current_permissions
        )

    db.commit()
    db.refresh(settings)

    return settings_to_response(settings)


# ============================================================
# RESET ALL SETTINGS
# ============================================================

@router.post(
    "/reset",
    response_model=UserSettingsResponse,
)
def reset_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    settings = get_or_create_settings(
        db,
        current_user,
    )

    defaults = UserSettings(
        user_id=current_user.id
    )

    reset_fields = [
        "display_name",
        "profile_picture",
        "timezone",
        "language",

        "assistant_name",
        "personality",
        "response_style",
        "response_length",
        "proactive_mode",

        "ai_provider",
        "ai_model",
        "fallback_provider",
        "fallback_model",
        "local_ai_enabled",
        "cloud_ai_enabled",

        "voice_enabled",
        "wake_word_enabled",
        "wake_word",
        "auto_speak",
        "speech_speed",
        "voice_name",

        "memory_enabled",
        "conversation_memory_enabled",
        "long_term_memory_enabled",
        "memory_confirmation",

        "notifications_enabled",
        "task_notifications",
        "reminder_notifications",
        "system_notifications",
        "proactive_notifications",

        "theme",
        "accent_color",
        "compact_mode",
    ]

    for field in reset_fields:

        setattr(
            settings,
            field,
            getattr(defaults, field),
        )

    PermissionService.reset_permissions(
        settings
    )

    db.commit()
    db.refresh(settings)

    return settings_to_response(settings)


# ============================================================
# TOOL PERMISSIONS
# ============================================================

@router.get("/tools")
def get_tool_permissions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    settings = get_or_create_settings(
        db,
        current_user,
    )

    permissions = PermissionService.get_permissions(
        settings
    )

    return {
        "tool_permissions": permissions,
        "permission_levels": [
            "allowed",
            "confirmation_required",
            "disabled",
        ],
    }


# ============================================================
# GET ONE TOOL PERMISSION
# ============================================================

@router.get("/tool/{tool_name}")
def get_tool_permission(
    tool_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    settings = get_or_create_settings(
        db,
        current_user,
    )

    permissions = PermissionService.get_permissions(
        settings
    )

    if tool_name not in permissions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unknown tool: {tool_name}",
        )

    return {
        "tool": tool_name,
        "permission": permissions[tool_name],
    }


# ============================================================
# CHANGE ONE TOOL PERMISSION
# ============================================================

@router.put("/tool/{tool_name}")
def update_tool_permission(
    tool_name: str,
    permission: ToolPermission,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    settings = get_or_create_settings(
        db,
        current_user,
    )

    permissions = PermissionService.set_permission(
        settings,
        tool_name,
        permission,
    )

    db.commit()
    db.refresh(settings)

    return {
        "message": "Tool permission updated",
        "tool": tool_name,
        "permission": permissions[tool_name],
    }


# ============================================================
# CHANGE ALL TOOL PERMISSIONS
# ============================================================

@router.put("/tools/all")
def update_all_tool_permissions(
    permission: ToolPermission,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    settings = get_or_create_settings(
        db,
        current_user,
    )

    permissions = PermissionService.set_all_permissions(
        settings,
        permission,
    )

    db.commit()
    db.refresh(settings)

    return {
        "message": "All tool permissions updated",
        "permission": permission,
        "tool_permissions": permissions,
    }


# ============================================================
# RESET TOOL PERMISSIONS ONLY
# ============================================================

@router.post("/tools/reset")
def reset_tool_permissions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    settings = get_or_create_settings(
        db,
        current_user,
    )

    permissions = PermissionService.reset_permissions(
        settings
    )

    db.commit()
    db.refresh(settings)

    return {
        "message": "Tool permissions reset",
        "tool_permissions": permissions,
    }


# ============================================================
# ACTIVE MODEL
# ============================================================

@router.get("/active-model")
def get_active_model(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    settings = get_or_create_settings(
        db,
        current_user,
    )

    return {
        "provider": settings.ai_provider,
        "model": settings.ai_model,
        "local_enabled": settings.local_ai_enabled,
        "cloud_enabled": settings.cloud_ai_enabled,
        "fallback_provider": settings.fallback_provider,
        "fallback_model": settings.fallback_model,
    }
