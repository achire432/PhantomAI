from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from pydantic import BaseModel

from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User

from backend.app.services.image_service import (
    generate_image,
)

from backend.app.services.conversation import (
    create_conversation,
    add_message,
)

from backend.app.schemas.message import (
    MessageCreate,
)


router = APIRouter(
    prefix="/images",
    tags=["Images"],
)


# ============================================================
# REQUEST MODEL
# ============================================================

class ImageRequest(BaseModel):
    prompt: str
    provider: str = "stability"
    aspect_ratio: str = "1:1"


# ============================================================
# GENERATE IMAGE
# ============================================================

@router.post("/generate")
def generate_image_endpoint(
    request: ImageRequest,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    ),
):
    """
    Generate an image.

    Flow:

    1. Authenticate user.
    2. Validate prompt.
    3. Generate image through selected provider.
    4. Create conversation.
    5. Save user's request.
    6. Save PhantomAI response.
    7. Return image.
    """

    # --------------------------------------------------------
    # VALIDATE PROMPT
    # --------------------------------------------------------

    prompt = request.prompt.strip()

    if not prompt:
        raise HTTPException(
            status_code=400,
            detail=(
                "Image prompt cannot be empty."
            ),
        )

    # --------------------------------------------------------
    # GENERATE IMAGE
    # --------------------------------------------------------

    result = generate_image(
        prompt=prompt,
        provider=request.provider,
        aspect_ratio=request.aspect_ratio,
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=400,
            detail=result.get(
                "error",
                "Image generation failed.",
            ),
        )

    # --------------------------------------------------------
    # CREATE CONVERSATION
    # --------------------------------------------------------

    conversation = create_conversation(
        db,
        current_user,
        f"🎨 Image: {prompt[:50]}...",
    )

    # --------------------------------------------------------
    # SAVE USER PROMPT
    # --------------------------------------------------------

    prompt_message = MessageCreate(
        role="user",
        content=(
            f"Generate an image: {prompt}"
        ),
    )

    add_message(
        db,
        conversation,
        prompt_message,
    )

    # --------------------------------------------------------
    # SAVE ASSISTANT RESPONSE
    # --------------------------------------------------------

    ai_message = MessageCreate(
        role="assistant",
        content=(
            f"🎨 Generated image for: "
            f"'{prompt}'\n\n"
            f"Provider: "
            f"{result.get('provider', request.provider)}"
        ),
    )

    add_message(
        db,
        conversation,
        ai_message,
    )

    # --------------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------------

    return {
        "success": True,
        "image": result.get("image"),
        "prompt": prompt,
        "provider": result.get(
            "provider",
            request.provider,
        ),
        "format": result.get(
            "format",
            "base64",
        ),
        "conversation_id": conversation.id,
    }
