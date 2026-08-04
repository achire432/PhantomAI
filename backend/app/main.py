"""
PHANTOM AI - MAIN APPLICATION
=============================
This is the entry point for Phantom AI.

What This File Does:
1. Creates the FastAPI application
2. Connects all routers (auth, conversations, chat, upload, notes)
3. Creates database tables
4. Starts the server
"""

from fastapi import FastAPI
from backend.app.routers.auth import router as auth_router
from backend.app.routers.conversation import router as conversation_router
from backend.app.routers.chat import router as chat_router
from backend.app.routers.upload import router as upload_router
from backend.app.routers.notes import router as notes_router
from backend.app.database.database import engine
from backend.app.models import Base
from backend.app.routers.tasks import router as tasks_router
from backend.app.routers.system import router as system_router
from backend.app.routers.weather import router as weather_router
from backend.app.routers.calendar import router as calendar_router  # ← NEW

# Create all database tables
print("📊 Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Database tables ready!")

# Create the FastAPI application
app = FastAPI(
    title="Phantom AI API",
    description="The backend for Phantom AI - Your intelligent assistant",
    version="0.2.0"
)

# Include all routers
app.include_router(auth_router)
app.include_router(conversation_router)
app.include_router(chat_router)
app.include_router(upload_router)
app.include_router(notes_router)  # ← NEW
app.include_router(tasks_router) 
app.include_router(system_router) 
app.include_router(weather_router)
app.include_router(calendar_router) # ← NEW

@app.get("/")
def root():
    return {
        "message": "Welcome to Phantom AI",
        "version": "0.2.0",
        "status": "online"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "version": "0.2.0"
    }