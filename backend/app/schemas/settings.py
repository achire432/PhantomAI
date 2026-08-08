from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


# ============================================================
# TOOL PERMISSION TYPES
# ============================================================

ToolPermission = Literal[
    "allowed",
    "confirmation_required",
    "disabled",
]


# ============================================================
# PROFILE
# ============================================================

class ProfileSettings(BaseModel):
    display_name: Optional[str] = None
    profile_picture: Optional[str] = None
    timezone: str = "UTC"
    language: str = "en"


# ============================================================
# PHANTOMAI BEHAVIOUR
# ============================================================

class PhantomAIBehaviourSettings(BaseModel):
    assistant_name: str = "PhantomAI"
    personality: str = "helpful"
    response_style: str = "balanced"
    response_length: str = "medium"
    proactive_mode: bool = True


# ============================================================
# AI SETTINGS
# ============================================================

class AISettings(BaseModel):
    ai_provider: str = "local"
    ai_model: str = "qwen-4b"
    fallback_provider: str = "groq"
    fallback_model: str = "groq-llama3"
    local_ai_enabled: bool = True
    cloud_ai_enabled: bool = True


# ============================================================
# VOICE
# ============================================================

class VoiceSettings(BaseModel):
    voice_enabled: bool = True
    wake_word_enabled: bool = True
    wake_word: str = "Hey Phantom"
    auto_speak: bool = True
    speech_speed: int = 150
    voice_name: str = "default"


# ============================================================
# MEMORY
# ============================================================

class MemorySettings(BaseModel):
    memory_enabled: bool = True
    conversation_memory_enabled: bool = True
    long_term_memory_enabled: bool = True
    memory_confirmation: bool = True


# ============================================================
# NOTIFICATIONS
# ============================================================

class NotificationSettings(BaseModel):
    notifications_enabled: bool = True
    task_notifications: bool = True
    reminder_notifications: bool = True
    system_notifications: bool = True
    proactive_notifications: bool = True


# ============================================================
# APPEARANCE
# ============================================================

class AppearanceSettings(BaseModel):
    theme: str = "dark"
    accent_color: str = "#00d4ff"
    compact_mode: bool = False


# ============================================================
# COMPLETE TOOL PERMISSIONS
# ============================================================

class ToolPermissions(BaseModel):

    # AI / Intelligence
    web_search: ToolPermission = "allowed"
    calculator: ToolPermission = "allowed"
    code_analysis: ToolPermission = "allowed"
    markdown: ToolPermission = "allowed"

    # Files / Documents
    file_reading: ToolPermission = "allowed"
    file_management: ToolPermission = "allowed"
    file_upload: ToolPermission = "allowed"
    pdf: ToolPermission = "allowed"
    ocr: ToolPermission = "allowed"

    # Media
    image_understanding: ToolPermission = "allowed"
    image_generation: ToolPermission = "allowed"
    video_generation: ToolPermission = "allowed"

    # Productivity
    notes: ToolPermission = "allowed"
    tasks: ToolPermission = "allowed"
    calendar: ToolPermission = "allowed"
    reminders: ToolPermission = "allowed"

    # Communication
    email_reading: ToolPermission = "allowed"
    email_sending: ToolPermission = "allowed"

    # Computer / System
    application_launcher: ToolPermission = "allowed"
    terminal: ToolPermission = "allowed"
    database: ToolPermission = "allowed"
    system_info: ToolPermission = "allowed"
    git: ToolPermission = "allowed"

    # Memory / Context
    memory: ToolPermission = "allowed"
    context: ToolPermission = "allowed"

    # Voice
    voice: ToolPermission = "allowed"
    wake_word: ToolPermission = "allowed"

    # AI model management
    model_management: ToolPermission = "allowed"

    # Notifications / proactive
    notifications: ToolPermission = "allowed"
    proactive: ToolPermission = "allowed"

    # Data
    data: ToolPermission = "allowed"

    # Weather
    weather: ToolPermission = "allowed"


# ============================================================
# PARTIAL TOOL PERMISSION UPDATE
# ============================================================

class ToolPermissionsUpdate(BaseModel):

    web_search: Optional[ToolPermission] = None
    calculator: Optional[ToolPermission] = None
    code_analysis: Optional[ToolPermission] = None
    markdown: Optional[ToolPermission] = None

    file_reading: Optional[ToolPermission] = None
    file_management: Optional[ToolPermission] = None
    file_upload: Optional[ToolPermission] = None
    pdf: Optional[ToolPermission] = None
    ocr: Optional[ToolPermission] = None

    image_understanding: Optional[ToolPermission] = None
    image_generation: Optional[ToolPermission] = None
    video_generation: Optional[ToolPermission] = None

    notes: Optional[ToolPermission] = None
    tasks: Optional[ToolPermission] = None
    calendar: Optional[ToolPermission] = None
    reminders: Optional[ToolPermission] = None

    email_reading: Optional[ToolPermission] = None
    email_sending: Optional[ToolPermission] = None

    application_launcher: Optional[ToolPermission] = None
    terminal: Optional[ToolPermission] = None
    database: Optional[ToolPermission] = None
    system_info: Optional[ToolPermission] = None
    git: Optional[ToolPermission] = None

    memory: Optional[ToolPermission] = None
    context: Optional[ToolPermission] = None

    voice: Optional[ToolPermission] = None
    wake_word: Optional[ToolPermission] = None

    model_management: Optional[ToolPermission] = None

    notifications: Optional[ToolPermission] = None
    proactive: Optional[ToolPermission] = None

    data: Optional[ToolPermission] = None
    weather: Optional[ToolPermission] = None


# ============================================================
# FULL SETTINGS RESPONSE
# ============================================================

class UserSettingsResponse(BaseModel):

    # Profile
    display_name: Optional[str] = None
    profile_picture: Optional[str] = None
    timezone: str = "UTC"
    language: str = "en"

    # PhantomAI Behaviour
    assistant_name: str = "PhantomAI"
    personality: str = "helpful"
    response_style: str = "balanced"
    response_length: str = "medium"
    proactive_mode: bool = True

    # AI
    ai_provider: str = "local"
    ai_model: str = "qwen-4b"
    fallback_provider: str = "groq"
    fallback_model: str = "groq-llama3"
    local_ai_enabled: bool = True
    cloud_ai_enabled: bool = True

    # Voice
    voice_enabled: bool = True
    wake_word_enabled: bool = True
    wake_word: str = "Hey Phantom"
    auto_speak: bool = True
    speech_speed: int = 150
    voice_name: str = "default"

    # Memory
    memory_enabled: bool = True
    conversation_memory_enabled: bool = True
    long_term_memory_enabled: bool = True
    memory_confirmation: bool = True

    # Notifications
    notifications_enabled: bool = True
    task_notifications: bool = True
    reminder_notifications: bool = True
    system_notifications: bool = True
    proactive_notifications: bool = True

    # Appearance
    theme: str = "dark"
    accent_color: str = "#00d4ff"
    compact_mode: bool = False

    # Permissions
    tool_permissions: ToolPermissions = Field(
        default_factory=ToolPermissions
    )

    # Timestamps
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# SETTINGS UPDATE
# ============================================================

class UserSettingsUpdate(BaseModel):

    # Profile
    display_name: Optional[str] = None
    profile_picture: Optional[str] = None
    timezone: Optional[str] = None
    language: Optional[str] = None

    # PhantomAI Behaviour
    assistant_name: Optional[str] = None
    personality: Optional[str] = None
    response_style: Optional[str] = None
    response_length: Optional[str] = None
    proactive_mode: Optional[bool] = None

    # AI
    ai_provider: Optional[str] = None
    ai_model: Optional[str] = None
    fallback_provider: Optional[str] = None
    fallback_model: Optional[str] = None
    local_ai_enabled: Optional[bool] = None
    cloud_ai_enabled: Optional[bool] = None

    # Voice
    voice_enabled: Optional[bool] = None
    wake_word_enabled: Optional[bool] = None
    wake_word: Optional[str] = None
    auto_speak: Optional[bool] = None
    speech_speed: Optional[int] = None
    voice_name: Optional[str] = None

    # Memory
    memory_enabled: Optional[bool] = None
    conversation_memory_enabled: Optional[bool] = None
    long_term_memory_enabled: Optional[bool] = None
    memory_confirmation: Optional[bool] = None

    # Notifications
    notifications_enabled: Optional[bool] = None
    task_notifications: Optional[bool] = None
    reminder_notifications: Optional[bool] = None
    system_notifications: Optional[bool] = None
    proactive_notifications: Optional[bool] = None

    # Appearance
    theme: Optional[str] = None
    accent_color: Optional[str] = None
    compact_mode: Optional[bool] = None

    # Tool Permissions
    tool_permissions: Optional[ToolPermissionsUpdate] = None
