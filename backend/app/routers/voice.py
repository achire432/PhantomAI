"""
VOICE ROUTER
=============
Purpose: Handle voice API requests.

Endpoints:
- POST /voice/speak - Text-to-Speech
- POST /voice/listen - Speech-to-Text
- POST /voice/chat - Full voice chat (listen + AI + speak)
- GET /voice/wake/start - Start wake listener
- GET /voice/wake/stop - Stop wake listener
- GET /voice/wake/status - Check wake status

Why This Matters:
- Exposes voice functionality to users
- All requests require authentication
- Makes PhantomAI feel like JARVIS
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.models.conversation import Conversation
from backend.app.services.voice_service import (
    text_to_speech, speech_to_text, speak
)
from backend.app.services.voice_chat_service import voice_chat
from backend.app.services.wake_word_service import (
    start_wake_listener, stop_wake_listener, get_wake_status
)

class SpeakRequest(BaseModel):
    text: str

router = APIRouter(prefix="/voice", tags=["Voice"])


@router.post("/speak")
def speak_endpoint(
    request: SpeakRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Make PhantomAI speak.
    
    Example:
        POST /voice/speak
        {"text": "Hello, how can I help?"}
        
    Response:
        {"success": True, "text": "Hello, how can I help?", "spoken": True}
    """
    result = text_to_speech(request.text)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result


@router.post("/listen")
def listen_endpoint(
    current_user: User = Depends(get_current_user)
):
    """
    Listen for a voice command.
    
    How It Works:
    1. PhantomAI listens to microphone
    2. Converts speech to text
    3. Returns the text
    
    Example:
        You speak: "What is the weather?"
        Returns: {"success": True, "text": "what is the weather"}
    """
    result = speech_to_text()
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result


@router.post("/chat")
def voice_chat_endpoint(
    conversation_id: int = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Full voice chat with PhantomAI.
    
    How It Works:
    1. PhantomAI listens to you (Speech-to-Text)
    2. Converts speech to text
    3. Sends to AI
    4. Gets AI response
    5. Speaks back (Text-to-Speech)
    6. Saves to conversation history
    
    This is the JARVIS feature!
    
    Example:
        You speak: "What is the weather?"
        PhantomAI responds: "The weather is 27°C and sunny."
    
    Returns:
    {
        "success": True,
        "user_text": "what is the weather",
        "ai_response": "The weather is 27°C and sunny.",
        "conversation_id": 1
    }
    """
    result = voice_chat(db, current_user.id, conversation_id)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result


@router.get("/wake/start")
def start_wake(
    current_user: User = Depends(get_current_user)
):
    """
    Start the wake word listener.
    
    PhantomAI starts listening for "Hey Phantom" in the background.
    
    Example:
        GET /voice/wake/start
        
    Response:
        {"message": "Wake listener started"}
    """
    return start_wake_listener()


@router.get("/wake/stop")
def stop_wake(
    current_user: User = Depends(get_current_user)
):
    """
    Stop the wake word listener.
    
    Example:
        GET /voice/wake/stop
        
    Response:
        {"message": "Wake listener stopped"}
    """
    return stop_wake_listener()


@router.get("/wake/status")
def wake_status(
    current_user: User = Depends(get_current_user)
):
    """
    Check if wake listener is running.
    
    Example:
        GET /voice/wake/status
        
    Response:
        {"is_running": True, "is_listening": False}
    """
    return get_wake_status()