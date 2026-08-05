"""
SETTINGS SCHEMAS
=================
Purpose: Validate settings data for API requests.

Why This Matters:
- Ensures data is valid before saving
- Controls what data is exposed to users
- Prevents invalid values from corrupting settings
- Type safety for all settings operations

Which Files Use This:
- routers/settings.py (to validate requests)
- services/settings_service.py (to ensure data integrity)
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Literal
from datetime import datetime

# ============================================
# TOOL PERMISSION TYPE
# ============================================
ToolPermission = Literal["allowed", "confirmation_required", "disabled"]

# ============================================
# PROFILE SCHEMA
# ============================================
class ProfileSettings(BaseModel):
    display_name: Optional[str] = None
    profile_picture: Optional[str] = None
    timezone: str = "UTC"
    language: str = "en"

# ============================================
# PHANTOMAI BEHAVIOUR SCHEMA
# ============================================
class PhantomAIBehaviourSettings(BaseModel):
    assistant_name: str = "PhantomAI"
    personality: str = "helpful"  # helpful, professional, casual, witty
    response_style: str = "balanced"  # balanced, concise, detailed
    response_length: str = "medium"  # short, medium, long
    proactive_mode: bool = True

# ============================================
# AI SETTINGS SCHEMA
# ============================================
class AISettings(BaseModel):
    ai_provider: str = "local"
    ai_model: str = "qwen-4b"
    fallback_provider: str = "groq"
    fallback_model: str = "groq-llama3"
    local_ai_enabled: bool = True
    cloud_ai_enabled: bool = True

# ============================================
# VOICE SETTINGS SCHEMA
# ============================================
class VoiceSettings(BaseModel):
    voice_enabled: bool = True
    wake_word_enabled: bool = True
    wake_word: str = "Hey Phantom"
    auto_speak: bool = True
    speech_speed: int = 150
    voice_name: str = "default"

# ============================================
# MEMORY SETTINGS SCHEMA
# ============================================
class MemorySettings(BaseModel):
    memory_enabled: bool = True
    conversation_memory_enabled: bool = True
    long_term_memory_enabled: bool = True
    memory_confirmation: bool = True

# ============================================
# NOTIFICATION SETTINGS SCHEMA
# ============================================
class NotificationSettings(BaseModel):
    notifications_enabled: bool = True
    task_notifications: bool = True
    reminder_notifications: bool = True
    system_notifications: bool = True
    proactive_notifications: bool = True

# ============================================
# APPEARANCE SETTINGS SCHEMA
# ============================================
class AppearanceSettings(BaseModel):
    theme: str = "dark"  # dark, light, system
    accent_color: str = "#00d4ff"
    compact_mode: bool = False

# ============================================
# TOOL PERMISSIONS SCHEMA
# ============================================
class ToolPermissions(BaseModel):
    web_search: ToolPermission = "allowed"
    file_reading: ToolPermission = "allowed"
    file_management: ToolPermission = "confirmation_required"
    email_reading: ToolPermission = "allowed"
    email_sending: ToolPermission = "confirmation_required"
    terminal: ToolPermission = "disabled"  # DANGEROUS - disabled by default
    database: ToolPermission = "confirmation_required"
    application_launcher: ToolPermission = "allowed"
    calendar: ToolPermission = "allowed"
    memory: ToolPermission = "allowed"
    git: ToolPermission = "allowed"
    system_info: ToolPermission = "allowed"
    weather: ToolPermission = "allowed"
    ocr: ToolPermission = "allowed"
    image_generation: ToolPermission = "allowed"
    video_generation: ToolPermission = "allowed"
    calculator: ToolPermission = "allowed"
    notes: ToolPermission = "allowed"
    tasks: ToolPermission = "allowed"
    reminders: ToolPermission = "allowed"

# ============================================
# FULL SETTINGS SCHEMA
# ============================================
class UserSettingsResponse(BaseModel):
    """Full response schema for user settings."""
    
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
    
    # Tool Permissions
    tool_permissions: ToolPermissions = ToolPermissions()
    
    # Timestamps
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserSettingsUpdate(BaseModel):
    """Schema for updating settings (all fields optional)."""
    
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
    tool_permissions: Optional[ToolPermissions] = None