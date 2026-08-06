"""
OCR ROUTER
===========
Purpose: Handle image upload and text extraction.

Flow:
1. Receive image
2. Validate image type
3. Extract text with OCR
4. Create user-owned conversation
5. Save extracted text
6. Return extracted text
"""

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException,
)
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.services.ocr_service import extract_text_from_image_bytes
from backend.app.services.conversation import (
    create_conversation,
    add_message,
)
from backend.app.schemas.message import MessageCreate


router = APIRouter(
    prefix="/ocr",
    tags=["OCR"]
)


@router.post("/")
async def extract_text(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Extract text from an uploaded image.
    """

    allowed_types = {
        "image/png",
        "image/jpeg",
        "image/jpg",
        "image/bmp",
        "image/tiff",
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Use PNG, JPG, BMP, or TIFF."
        )

    try:
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="Image must have a filename."
            )

        # Read image
        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(
                status_code=400,
                detail="The uploaded image is empty."
            )

        # Extract text
        result = extract_text_from_image_bytes(image_bytes)

        if not result.get("success"):
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "OCR extraction failed.")
            )

        extracted_text = result.get("text", "")

        # Create conversation owned by current user
        conversation = create_conversation(
            db,
            current_user,
            f"📷 Image: {file.filename}"
        )

        # Save OCR result
        message = MessageCreate(
            role="assistant",
            content=(
                f"📷 Extracted text from '{file.filename}':\n\n"
                f"{extracted_text}"
            )
        )

        add_message(
            db,
            conversation,
            message
        )

        return {
            "success": True,
            "text": extracted_text,
            "conversation_id": conversation.id,
            "file_name": file.filename
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"OCR processing failed: {str(e)}"
        )

    finally:
        await file.close()
