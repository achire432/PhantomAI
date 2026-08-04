"""
PHANTOM AI - MAIN APPLICATION
=============================
This is the entry point for Phantom AI.

ROUTERS INCLUDED:
- auth: Login, Register, JWT
- conversations: Create, list, get conversations
- chat: Send messages, get history
- upload: File uploads
- notes: Create, read, update, delete notes
- tasks: Create, read, update, delete tasks
- system: System information (CPU, RAM, etc.)
- weather: Current weather
- calendar: Events management
- reminders: Set and manage reminders
- email: Read, summarize, send emails
- ocr: Extract text from images
- markdown: Read and render .md files
- git: Status, log, branches
- database: Query PostgreSQL safely
- code: Analyze Python code
- apps: Launch applications
- files: File management
- terminal: Run safe commands
- proactive: System alerts
- context: User preferences
- memory: Long-term memory
- voice: Speech-to-Text, Text-to-Speech, Voice Chat, Wake Word
- notifications: System notifications
- data: Export/Import data

VERSION: 0.5.0
"""

from fastapi import FastAPI
from backend.app.routers.auth import router as auth_router
from backend.app.routers.conversation import router as conversation_router
from backend.app.routers.chat import router as chat_router
from backend.app.routers.upload import router as upload_router
from backend.app.routers.notes import router as notes_router
from backend.app.routers.tasks import router as tasks_router
from backend.app.routers.system import router as system_router
from backend.app.routers.weather import router as weather_router
from backend.app.routers.calendar import router as calendar_router
from backend.app.routers.reminders import router as reminders_router
from backend.app.routers.email import router as email_router
from backend.app.routers.ocr import router as ocr_router
from backend.app.routers.markdown import router as markdown_router
from backend.app.routers.git import router as git_router
from backend.app.routers.database import router as database_router
from backend.app.routers.code import router as code_router
from backend.app.routers.apps import router as apps_router
from backend.app.routers.files import router as files_router
from backend.app.routers.terminal import router as terminal_router
from backend.app.routers.proactive import router as proactive_router
from backend.app.routers.context import router as context_router
from backend.app.routers.memory import router as memory_router
from backend.app.routers.voice import router as voice_router
from backend.app.routers.notifications import router as notifications_router
from backend.app.routers.data import router as data_router
from backend.app.routers.pdf import router as pdf_router
from backend.app.routers.models import router as models_router
from backend.app.routers.images import router as images_router
from backend.app.routers.api_keys import router as api_keys_router
from backend.app.routers.video import router as video_router


from backend.app.database.database import engine
from backend.app.models import Base

# ============================================
# CREATE DATABASE TABLES
# ============================================
print("📊 Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Database tables ready!")

# ============================================
# CREATE FASTAPI APPLICATION
# ============================================
app = FastAPI(
    title="Phantom AI API",
    description="The backend for Phantom AI - Your intelligent assistant",
    version="0.5.0"
)

# ============================================
# INCLUDE ALL ROUTERS
# ============================================
app.include_router(auth_router)          # Authentication
app.include_router(conversation_router)  # Conversations
app.include_router(chat_router)          # Chat
app.include_router(upload_router)        # File Upload
app.include_router(notes_router)         # Notes
app.include_router(tasks_router)         # Tasks
app.include_router(system_router)        # System Info
app.include_router(weather_router)       # Weather
app.include_router(calendar_router)      # Calendar
app.include_router(reminders_router)     # Reminders
app.include_router(email_router)         # Email
app.include_router(ocr_router)           # OCR
app.include_router(markdown_router)      # Markdown
app.include_router(git_router)           # Git
app.include_router(database_router)      # Database
app.include_router(code_router)          # Code Analysis
app.include_router(apps_router)          # Application Launcher
app.include_router(files_router)         # File Management
app.include_router(terminal_router)      # Terminal
app.include_router(proactive_router)     # Proactive Assistant
app.include_router(context_router)       # Context Engine
app.include_router(memory_router)        # Long-Term Memory
app.include_router(voice_router)         # Voice Features
app.include_router(notifications_router) # Notifications
app.include_router(data_router)          # Export/Import Data
app.include_router(pdf_router)           # PDF Generation
app.include_router(models_router)        # Model Management
app.include_router(images_router)        # Image Processing
app.include_router(api_keys_router)      # API Keys
app.include_router(video_router)         # Video Generation
# ============================================
# ROOT ENDPOINTS
# ============================================

@app.get("/")
def root():
    return {
        "message": "Welcome to Phantom AI",
        "version": "0.5.0",
        "status": "online",
        "routers": [
            "auth",
            "conversations",
            "chat",
            "upload",
            "notes",
            "tasks",
            "system",
            "weather",
            "calendar",
            "reminders",
            "email",
            "ocr",
            "markdown",
            "git",
            "database",
            "code",
            "apps",
            "files",
            "terminal",
            "proactive",
            "context",
            "memory",
            "voice",
            "notifications",
            "data"
            "pdf",
            "models",
            "images",
            "api_keys",
            "video"
        ]
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "version": "0.5.0"
    }

@app.get("/routers")
def list_routers():
    return {
        "routers": [
            {"name": "Authentication", "prefix": "/auth"},
            {"name": "Conversations", "prefix": "/conversations"},
            {"name": "Chat", "prefix": "/chat"},
            {"name": "Upload", "prefix": "/upload"},
            {"name": "Notes", "prefix": "/notes"},
            {"name": "Tasks", "prefix": "/tasks"},
            {"name": "System", "prefix": "/system"},
            {"name": "Weather", "prefix": "/weather"},
            {"name": "Calendar", "prefix": "/calendar"},
            {"name": "Reminders", "prefix": "/reminders"},
            {"name": "Email", "prefix": "/email"},
            {"name": "OCR", "prefix": "/ocr"},
            {"name": "Markdown", "prefix": "/markdown"},
            {"name": "Git", "prefix": "/git"},
            {"name": "Database", "prefix": "/database"},
            {"name": "Code Analysis", "prefix": "/code"},
            {"name": "Applications", "prefix": "/apps"},
            {"name": "Files", "prefix": "/files"},
            {"name": "Terminal", "prefix": "/terminal"},
            {"name": "Proactive", "prefix": "/proactive"},
            {"name": "Context", "prefix": "/context"},
            {"name": "Memory", "prefix": "/memory"},
            {"name": "Voice", "prefix": "/voice"},
            {"name": "Notifications", "prefix": "/notifications"},
            {"name": "Data", "prefix": "/data"},
            {"name": "PDF", "prefix": "/pdf"},
            {"name": "Models", "prefix": "/models"},
            {"name": "Images", "prefix": "/images"},
            {"name": "API Keys", "prefix": "/api_keys"},
            {"name": "Video", "prefix": "/video"}
        ]
    }