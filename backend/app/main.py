"""
PhantomAI Backend Application Entry Point
=========================================

This file is the "Engine Room" of PhantomAI.

It is built using FastAPI, a high-performance Python web framework.

ARCHITECTURAL IMPORTANCE:

1. SINGLE POINT OF ENTRY
   When you run:
       uvicorn backend.app.main:app --reload

   this file starts the entire backend server.

2. ROUTER AGGREGATOR
   PhantomAI has many independent features. Each feature lives in its
   own router file. This file imports and registers those routers.

3. DATABASE INITIALIZATION
   PostgreSQL is connected through the database module and SQLAlchemy
   creates any missing tables when the application starts.

4. SECURITY / CORS
   CORS allows the React frontend running on port 5173 to communicate
   with the FastAPI backend.

5. API DISCOVERY
   The root endpoints provide basic information about PhantomAI,
   its health status, and available routers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# ============================================================
# ROUTER IMPORTS
# ============================================================

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
from backend.app.routers.settings import router as settings_router
from backend.app.routers.calculator import router as calculator_router
from backend.app.routers.web import router as web_router


# ============================================================
# DATABASE IMPORTS
# ============================================================

from backend.app.database.database import engine
from backend.app.models import Base


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

print("📊 Creating database tables...")

Base.metadata.create_all(bind=engine)

print("✅ Database tables ready!")


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Phantom AI API",
    description="The backend for Phantom AI - Your intelligent assistant",
    version="0.5.0",
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

"""
CORS allows the React frontend to communicate with the FastAPI backend.

Development frontend:
http://localhost:5173

Backend:
http://127.0.0.1:8000
"""

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REGISTER ROUTERS
# ============================================================

# Authentication
app.include_router(auth_router)

# Conversations
app.include_router(conversation_router)

# Core AI chat
app.include_router(chat_router)

# File upload
app.include_router(upload_router)

# Productivity
app.include_router(notes_router)
app.include_router(tasks_router)
app.include_router(calendar_router)
app.include_router(reminders_router)

# Email
app.include_router(email_router)

# System
app.include_router(system_router)

# Utilities
app.include_router(weather_router)
app.include_router(calculator_router)

# Documents / processing
app.include_router(ocr_router)
app.include_router(markdown_router)
app.include_router(pdf_router)

# Development tools
app.include_router(git_router)
app.include_router(database_router)
app.include_router(code_router)
app.include_router(terminal_router)

# Applications / files
app.include_router(apps_router)
app.include_router(files_router)

# AI / context / memory
app.include_router(proactive_router)
app.include_router(context_router)
app.include_router(memory_router)

# Voice / notifications
app.include_router(voice_router)
app.include_router(notifications_router)

# Data
app.include_router(data_router)

# Models / AI settings
app.include_router(models_router)
app.include_router(settings_router)
app.include_router(web_router)

# Media
app.include_router(images_router)
app.include_router(video_router)

# API keys
app.include_router(api_keys_router)


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():
    """
    Root endpoint.

    Returns basic information about PhantomAI and its available
    backend features.
    """

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
            "calculator",
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
            "data",
            "pdf",
            "models",
            "images",
            "api_keys",
            "video",
            "settings",
        ],
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():
    """
    Health check endpoint.

    Used to confirm that the PhantomAI backend is running.
    """

    return {
        "status": "healthy",
        "version": "0.5.0",
    }


# ============================================================
# ROUTER DISCOVERY
# ============================================================

@app.get("/routers")
def list_routers():
    """
    Lists all available routers and their URL prefixes.

    Useful for frontend discovery and debugging.
    """

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
            {"name": "Calculator", "prefix": "/calculator"},
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
            {"name": "Video", "prefix": "/video"},
            {"name": "Settings", "prefix": "/settings"},
        ]
    }