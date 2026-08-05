"""
SETTINGS MODEL
===============
Purpose: Store comprehensive user settings.

Why This Matters:
- Users have different preferences
- PhantomAI should adapt to each user
- Settings persist across sessions
- One central place for all configuration

What It Stores:
- Profile: name, timezone, language
- PhantomAI Behaviour: personality, response style
- AI: which models to use
- Voice: enable/disable, wake word
- Memory: enable/disable
- Notifications: what to alert about
- Appearance: dark/light mode
- Tool Permissions: what tools are allowed

What Would Happen Without This:
- Everyone gets the same experience
- No personalization
- Tools can't be controlled per user
- PhantomAI feels generic

Which Files Use This:
- services/settings_service.py (to access settings)
- routers/settings.py (API endpoints)
- ai.py (for response style)
- tools/ (for permissions)
- voice/ (for voice settings)
"""

from sqlalchemy import String, Integer, DateTime, Text, ForeignKey, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column,relationship
from datetime import datetime

from backend.app.database.database import Base


class UserSettings(Base):
    """
    This is the Settings table in your database.
    
    One row per user (one-to-one relationship).
    Each user has their own settings.
    """
    __tablename__ = "user_settings"

    # ============================================
    # IDENTIFIER
    # ============================================
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    # ============================================
    # PROFILE (Who the user is)
    # ============================================
    display_name: Mapped[str] = mapped_column(String(100), nullable=True)
    profile_picture: Mapped[str] = mapped_column(String(500), nullable=True)  # URL or path
    timezone: Mapped[str] = mapped_column(String(50), default="UTC")
    language: Mapped[str] = mapped_column(String(10), default="en")

    # ============================================
    # PHANTOMAI BEHAVIOUR (How PhantomAI acts)
    # ============================================
    assistant_name: Mapped[str] = mapped_column(String(50), default="PhantomAI")
    personality: Mapped[str] = mapped_column(String(50), default="helpful")  # helpful, professional, casual, witty
    response_style: Mapped[str] = mapped_column(String(50), default="balanced")  # balanced, concise, detailed
    response_length: Mapped[str] = mapped_column(String(20), default="medium")   # short, medium, long
    proactive_mode: Mapped[bool] = mapped_column(Boolean, default=True)  # Does PhantomAI proactively alert you?

    # ============================================
    # AI SETTINGS (Which AI models to use)
    # ============================================
    ai_provider: Mapped[str] = mapped_column(String(50), default="local")  # local, groq, openai, anthropic
    ai_model: Mapped[str] = mapped_column(String(50), default="qwen-4b")
    fallback_provider: Mapped[str] = mapped_column(String(50), default="groq")
    fallback_model: Mapped[str] = mapped_column(String(50), default="groq-llama3")
    local_ai_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    cloud_ai_enabled: Mapped[bool] = mapped_column(Boolean, default=True)

    # ============================================
    # VOICE SETTINGS (How PhantomAI speaks)
    # ============================================
    voice_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    wake_word_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    wake_word: Mapped[str] = mapped_column(String(50), default="Hey Phantom")
    auto_speak: Mapped[bool] = mapped_column(Boolean, default=True)  # Automatically speak responses
    speech_speed: Mapped[int] = mapped_column(Integer, default=150)  # Words per minute
    voice_name: Mapped[str] = mapped_column(String(50), default="default")

    # ============================================
    # MEMORY SETTINGS (What PhantomAI remembers)
    # ============================================
    memory_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    conversation_memory_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    long_term_memory_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    memory_confirmation: Mapped[bool] = mapped_column(Boolean, default=True)  # Ask before storing important info

    # ============================================
    # NOTIFICATION SETTINGS (What PhantomAI alerts you about)
    # ============================================
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    task_notifications: Mapped[bool] = mapped_column(Boolean, default=True)
    reminder_notifications: Mapped[bool] = mapped_column(Boolean, default=True)
    system_notifications: Mapped[bool] = mapped_column(Boolean, default=True)
    proactive_notifications: Mapped[bool] = mapped_column(Boolean, default=True)

    # ============================================
    # APPEARANCE SETTINGS (How it looks)
    # ============================================
    theme: Mapped[str] = mapped_column(String(20), default="dark")  # dark, light, system
    accent_color: Mapped[str] = mapped_column(String(20), default="#00d4ff")
    compact_mode: Mapped[bool] = mapped_column(Boolean, default=False)

    # ============================================
    # TOOL PERMISSIONS (What tools PhantomAI can use)
    # ============================================
    tool_permissions: Mapped[dict] = mapped_column(JSON, default={
        # Permission levels: "allowed", "confirmation_required", "disabled"
        "web_search": "allowed",
        "file_reading": "allowed",
        "file_management": "confirmation_required",
        "email_reading": "allowed",
        "email_sending": "confirmation_required",
        "terminal": "disabled",  # DANGEROUS - keep disabled by default
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
    })

    # ============================================
    # TIMESTAMPS
    # ============================================
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ============================================
    # RELATIONSHIP
    # ============================================
    # The user relationship is defined in the User model

    user = relationship("User", back_populates="settings")