"""
IMAGE ROUTER
=============
Purpose: Handle image generation API requests.

Flow:
1. Authenticate user
2. Generate image
3. Create user-owned conversation
4. Save user's prompt
5. Save PhantomAI response
6. Return generated image
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.services.image_service import generate_image
from backend.app.services.conversation import (
    create_conversation,
    add_message,
)
from backend.app.schemas.message import MessageCreate


class ImageRequest(BaseModel):
    prompt: str
    provider: str = "stability"


router = APIRouter(
    prefix="/images",
    tags=["Images"]
)


@router.post("/generate")
def generate_image_endpoint(
    request: ImageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate an image from a text description.
    """

    # Validate prompt
    if not request.prompt.strip():
        raise HTTPException(
            status_code=400,
            detail="Image prompt cannot be empty."
        )

    # Generate image
    result = generate_image(
        request.prompt,
        request.provider
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=400,
            detail=result.get(
                "error",
                "Image generation failed."
            )
        )

    # Create conversation owned by current user
    conversation = create_conversation(
        db,
        current_user,
        f"🎨 Image: {request.prompt[:50]}..."
    )

    # Save user prompt
    prompt_message = MessageCreate(
        role="user",
        content=f"Generate an image: {request.prompt}"
    )

    add_message(
        db,
        conversation,
        prompt_message
    )

    # Save AI response
    ai_message = MessageCreate(
        role="assistant",
        content=(
            f"🎨 Generated image for: "
            f"'{request.prompt}'\n\n"
            "Image data is available in the response."
        )
    )

    add_message(
        db,
        conversation,
        ai_message
    )

    return {
        "success": True,
        "image": result.get("image"),
        "prompt": request.prompt,
        "provider": request.provider,
        "conversation_id": conversation.id
    }
