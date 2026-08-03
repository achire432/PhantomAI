from fastapi import FastAPI
from backend.app.routers.auth import router as auth_router
from backend.app.routers.conversation import router as conversation_router
from backend.app.routers.chat import router as chat_router
app = FastAPI(
    title="Phantom AI API",
    description="The backend for Phantom AI - Your intelligent assistant",
    version="0.1.0"
)

# Include routers
app.include_router(auth_router)
app.include_router(conversation_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Phantom AI",
        "version": "0.1.0"
    }