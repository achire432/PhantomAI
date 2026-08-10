"""
PHANTOM AI - MAIN APPLICATION BACKEND
=====================================
This file is the "Engine Room" of PhantomAI.
It is built using FastAPI, a high-performance Python web framework.

ARCHITECTURAL IMPORTANCE:
1. SINGLE POINT OF ENTRY: When you run `uvicorn main:app --reload`, this file 
   starts the entire backend server.

2. ROUTER AGGREGATOR: Instead of cramming 33 different functionalities into one 
   huge file, we split them into separate "routers" (files). This file simply 
   imports them and glues them together.

3. DATABASE CONNECTION: It connects to PostgreSQL and creates all required 
   tables automatically when the server starts.

4. SECURITY (CORS): It configures Cross-Origin Resource Sharing, allowing your 
   React Frontend (running on port 5173) to securely talk to this backend.

5. API VERSIONING: It defines the root endpoints (/, /health, /routers) so 
   users can check if the AI is alive and what features are available.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- IMPORT ROUTERS ---
# Each router corresponds to a specific feature module.
# They are kept in separate files to keep the code clean, scalable, and maintainable.
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

# --- DATABASE IMPORTS ---
# This connects to your PostgreSQL database and handles the ORM (Object-Relational Mapping)
from backend.app.database.database import engine
from backend.app.models import Base

# ============================================
# 1. DATABASE INITIALIZATION
# ============================================
print("📊 Creating database tables...")
# `create_all` checks if tables exist in PostgreSQL. If they don't, it creates them.
# This ensures your DB is ready before the API starts accepting requests.
Base.metadata.create_all(bind=engine)
print("✅ Database tables ready!")

# ============================================
# 2. CREATE FASTAPI APPLICATION INSTANCE
# ============================================
app = FastAPI(
    title="Phantom AI API",
    description="The backend for Phantom AI - Your intelligent assistant",
    version="0.5.0"
)

# ============================================
# 3. REGISTER ROUTERS
# ============================================
# This is where we "plug in" all the features. 
# Every router has a specific prefix (e.g., /auth, /chat) defined inside its own file.
app.include_router(auth_router)          # Authentication (Login, Register, JWT)
app.include_router(conversation_router)  # Conversations (History management)
app.include_router(chat_router)          # Chat (The core AI Qwen3-4B interaction)
app.include_router(upload_router)        # File Upload (PDFs, Images, etc.)
app.include_router(notes_router)         # Notes (CRUD operations)
app.include_router(tasks_router)         # Tasks (CRUD operations)
app.include_router(system_router)        # System Info (CPU, RAM usage)
app.include_router(weather_router)       # Weather (Real-time weather data)
app.include_router(calendar_router)      # Calendar (Event scheduling)
app.include_router(reminders_router)     # Reminders (Set alerts)
app.include_router(email_router)         # Email (Read, summarize, send emails)
app.include_router(ocr_router)           # OCR (Extract text from images)
app.include_router(markdown_router)      # Markdown (Read and render .md files)
app.include_router(git_router)           # Git (Status, log, branches)
app.include_router(database_router)      # Database (Safe PostgreSQL queries)
app.include_router(code_router)          # Code Analysis (Python code evaluation)
app.include_router(apps_router)          # Apps (Launch other applications)
app.include_router(files_router)         # Files (File management)
app.include_router(terminal_router)      # Terminal (Run safe commands)
app.include_router(proactive_router)     # Proactive (System alerts)
app.include_router(context_router)       # Context (User preferences)
app.include_router(memory_router)        # Memory (Long-term AI memory)
app.include_router(voice_router)         # Voice (Speech-to-Text, Text-to-Speech)
app.include_router(notifications_router) # Notifications (System notifications)
app.include_router(data_router)          # Data (Export/Import data)
app.include_router(pdf_router)           # PDF (Generate PDF reports)
app.include_router(models_router)        # Models (Manage AI model parameters)
app.include_router(images_router)        # Images (Image processing)
app.include_router(api_keys_router)      # API Keys (Manage external API keys)
app.include_router(video_router)         # Video (Video generation)
app.include_router(settings_router)      # Settings (Global application settings)
app.include_router(calculator_router)    # Calculator (Mathematical calculations)
# ============================================
# 4. ROOT / DISCOVERY ENDPOINTS
# ============================================
# These endpoints allow users and the frontend to check if the server is alive.

@app.get("/")
def root():
    """Root endpoint. Returns basic information about the system."""
    return {
        "message": "Welcome to Phantom AI",
        "version": "0.5.0",
        "status": "online",
        # Note: Fixed missing comma between "data" and "pdf" below.
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
            "data",
            "pdf",          # <--- Added missing comma here
            "models",
            "images",
            "api_keys",
            "video",
            "settings"
        ]
    }

@app.get("/health")
def health():
    """Health check endpoint. Used to monitor if the server is running correctly."""
    return {
        "status": "healthy",
        "version": "0.5.0"
    }

@app.get("/routers")
def list_routers():
    """Lists all available routers and their URL prefixes for frontend discovery."""
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
            {"name": "Video", "prefix": "/video"},
            {"name": "Settings", "prefix": "/settings"}
        ]
    }

# ============================================
# 5. CORS MIDDLEWARE CONFIGURATION
# ============================================
# CORS (Cross-Origin Resource Sharing) is a browser security feature.
# It blocks web pages from making requests to different domains.
# 
# By adding this middleware, we explicitly tell the browser:
# "It is safe to allow requests from http://localhost:5173 (your React App)
# to access this FastAPI backend."
# 
# Without this, your frontend will get a "Network Error" when trying to log in or chat.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # The exact URL of your Vite dev server
    allow_credentials=True,                   # Allows cookies/sessions to be passed
    allow_methods=["*"],                      # Allows GET, POST, PUT, DELETE
    allow_headers=["*"],                      # Allows any HTTP headers
)