"""
IMAGE ROUTER
=============
Purpose: Handle image generation API requests.

Endpoints:
- POST /images/generate - Generate an image from text
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.services.image_service import generate_image
from backend.app.services.conversation import create_conversation, add_message
from backend.app.schemas.message import MessageCreate

class ImageRequest(BaseModel):
    prompt: str
    provider: str = "stability"  # Default to stability (free)

router = APIRouter(prefix="/images", tags=["Images"])

@router.post("/generate")
def generate_image_endpoint(
    request: ImageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate an image from a text description.
    
    Example:
        POST /images/generate
        {"prompt": "A cat wearing a space suit", "provider": "stability"}
    """
    
    result = generate_image(request.prompt, request.provider)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    # Create a conversation for the image generation
    conversation = create_conversation(
        db,
        current_user,
        f"🎨 Image: {request.prompt[:50]}..."
    )
    
    # Save the prompt
    prompt_message = MessageCreate(
        role="user",
        content=f"Generate an image: {request.prompt}"
    )
    add_message(db, conversation.id, prompt_message)
    
    # Save the response
    ai_message = MessageCreate(
        role="assistant",
        content=f"🎨 Generated image for: '{request.prompt}'\n\nImage data is available in the response."
    )
    add_message(db, conversation.id, ai_message)
    
    return {
        "success": True,
        "image": result.get("image"),
        "prompt": request.prompt,
        "provider": request.provider,
        "conversation_id": conversation.id
    }