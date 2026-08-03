"""
PHANTOM AI - MAIN APPLICATION
=============================
This is the entry point for Phantom AI.

What This File Does:
1. Creates the FastAPI application
2. Connects all routers (auth, conversations, chat, upload)
3. Creates database tables
4. Starts the server

Why We Structure It This Way:
- All routers are in one place
- Easy to add new features
- Clean and organized
"""

from fastapi import FastAPI
from backend.app.routers.auth import router as auth_router
from backend.app.routers.conversation import router as conversation_router
from backend.app.routers.chat import router as chat_router
from backend.app.routers.upload import router as upload_router
from backend.app.database.database import engine
from backend.app.models import Base

# Create all database tables
# This runs when the server starts
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
# Each router handles a different part of the API
app.include_router(auth_router)          # Login, Register
app.include_router(conversation_router)  # Conversations
app.include_router(chat_router)          # Chat messages
app.include_router(upload_router)        # File uploads

@app.get("/")
def root():
    """
    Root endpoint - check if the server is running.
    """
    return {
        "message": "Welcome to Phantom AI",
        "version": "0.2.0",
        "status": "online"
    }

@app.get("/health")
def health():
    """
    Health check endpoint - for monitoring.
    """
    return {
        "status": "healthy",
        "version": "0.2.0"
    }