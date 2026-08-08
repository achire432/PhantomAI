from typing import Literal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.app.models.settings import UserSettings


PermissionLevel = Literal[
    "allowed",
    "confirmation_required",
    "disabled",
]


class PermissionService:
    """
    Central permission system for PhantomAI.

    Every PhantomAI tool should eventually check this
    service before executing.
    """

    VALID_LEVELS = {
        "allowed",
        "confirmation_required",
        "disabled",
    }

    # ========================================================
    # DEFAULT PERMISSIONS
    # ========================================================

    DEFAULT_PERMISSIONS = {
        # ----------------------------------------------------
        # AI / INFORMATION
        # ----------------------------------------------------

        "web_search": "allowed",

        "file_reading": "allowed",

        "file_management": "confirmation_required",

        "ocr": "allowed",

        # ----------------------------------------------------
        # COMMUNICATION
        # ----------------------------------------------------

        "email_reading": "allowed",

        "email_sending": "confirmation_required",

        "notifications": "allowed",

        # ----------------------------------------------------
        # PRODUCTIVITY
        # ----------------------------------------------------

        "calendar": "allowed",

        "tasks": "allowed",

        "reminders": "allowed",

        "notes": "allowed",

        "memory": "allowed",

        # ----------------------------------------------------
        # DEVELOPMENT
        # ----------------------------------------------------

        "git": "allowed",

        "code_analysis": "allowed",

        "database": "confirmation_required",

        # ----------------------------------------------------
        # COMPUTER CONTROL
        # ----------------------------------------------------

        "application_launcher": "allowed",

        "terminal": "disabled",

        # ----------------------------------------------------
        # SYSTEM
        # ----------------------------------------------------

        "system_info": "allowed",

        # ----------------------------------------------------
        # AI GENERATION
        # ----------------------------------------------------

        "image_generation": "allowed",

        "video_generation": "allowed",

        "calculator": "allowed",

        # ----------------------------------------------------
        # DOCUMENTS
        # ----------------------------------------------------

        "pdf": "allowed",
    }

    # ========================================================
    # GET ALL PERMISSIONS
    # ========================================================

    @classmethod
    def get_permissions(
        cls,
        settings: UserSettings,
    ) -> dict:

        """
        Return the complete permission map.

        Existing user permissions are preserved.

        Newly-added PhantomAI tools automatically receive
        their default permission.
        """

        stored_permissions = (
            settings.tool_permissions or {}
        )

        merged_permissions = (
            cls.DEFAULT_PERMISSIONS.copy()
        )

        merged_permissions.update(
            stored_permissions
        )

        return merged_permissions

    # ========================================================
    # GET ONE PERMISSION
    # ========================================================

    @classmethod
    def get_permission(
        cls,
        settings: UserSettings,
        tool_name: str,
    ) -> PermissionLevel:

        permissions = cls.get_permissions(
            settings
        )

        return permissions.get(
            tool_name,
            "disabled",
        )

    # ========================================================
    # VALIDATE PERMISSION LEVEL
    # ========================================================

    @classmethod
    def validate_level(
        cls,
        level: str,
    ) -> None:

        if level not in cls.VALID_LEVELS:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Invalid permission level "
                    f"'{level}'. "
                    f"Allowed values: "
                    f"{', '.join(sorted(cls.VALID_LEVELS))}"
                ),
            )

    # ========================================================
    # SET ONE PERMISSION
    # ========================================================

    @classmethod
    def set_permission(
        cls,
        settings: UserSettings,
        tool_name: str,
        level: PermissionLevel,
    ) -> dict:

        cls.validate_level(level)

        permissions = cls.get_permissions(
            settings
        )

        if tool_name not in permissions:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unknown tool: {tool_name}",
            )

        permissions[tool_name] = level

        settings.tool_permissions = permissions

        return permissions

    # ========================================================
    # SET ALL PERMISSIONS
    # ========================================================

    @classmethod
    def set_all_permissions(
        cls,
        settings: UserSettings,
        level: PermissionLevel,
    ) -> dict:

        cls.validate_level(level)

        permissions = cls.get_permissions(
            settings
        )

        for tool_name in permissions:
            permissions[tool_name] = level

        settings.tool_permissions = permissions

        return permissions

    # ========================================================
    # RESET PERMISSIONS
    # ========================================================

    @classmethod
    def reset_permissions(
        cls,
        settings: UserSettings,
    ) -> dict:

        settings.tool_permissions = (
            cls.DEFAULT_PERMISSIONS.copy()
        )

        return settings.tool_permissions

    # ========================================================
    # CHECK PERMISSION
    # ========================================================

    @classmethod
    def check(
        cls,
        settings: UserSettings,
        tool_name: str,
    ) -> PermissionLevel:

        return cls.get_permission(
            settings,
            tool_name,
        )

    # ========================================================
    # REQUIRE ALLOWED
    # ========================================================

    @classmethod
    def require_allowed(
        cls,
        settings: UserSettings,
        tool_name: str,
    ) -> bool:

        permission = cls.get_permission(
            settings,
            tool_name,
        )

        if permission == "disabled":

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "tool_disabled",
                    "tool": tool_name,
                    "message": (
                        f"The '{tool_name}' tool "
                        "is disabled in your "
                        "PhantomAI settings."
                    ),
                },
            )

        if permission == "confirmation_required":

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "confirmation_required",
                    "tool": tool_name,
                    "message": (
                        f"The '{tool_name}' tool "
                        "requires user confirmation "
                        "before execution."
                    ),
                },
            )

        return True

    # ========================================================
    # IS ALLOWED
    # ========================================================

    @classmethod
    def is_allowed(
        cls,
        settings: UserSettings,
        tool_name: str,
    ) -> bool:

        return (
            cls.get_permission(
                settings,
                tool_name,
            )
            == "allowed"
        )

    # ========================================================
    # NEEDS CONFIRMATION
    # ========================================================

    @classmethod
    def needs_confirmation(
        cls,
        settings: UserSettings,
        tool_name: str,
    ) -> bool:

        return (
            cls.get_permission(
                settings,
                tool_name,
            )
            == "confirmation_required"
        )

    # ========================================================
    # IS DISABLED
    # ========================================================

    @classmethod
    def is_disabled(
        cls,
        settings: UserSettings,
        tool_name: str,
    ) -> bool:

        return (
            cls.get_permission(
                settings,
                tool_name,
            )
            == "disabled"
        )