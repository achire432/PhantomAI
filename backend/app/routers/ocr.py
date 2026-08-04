"""
OCR ROUTER
===========
Purpose: Handle image upload and text extraction.

Endpoint:
- POST /ocr/ - Upload image, get text

Why This Matters:
- Exposes OCR to users
- Only authenticated users can use it
- Creates a conversation with the text
"""

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.services.ocr_service import extract_text_from_image_bytes
from backend.app.services.conversation import create_conversation, add_message
from backend.app.schemas.message import MessageCreate

router = APIRouter(prefix="/ocr", tags=["OCR"])

@router.post("/")
async def extract_text(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Extract text from an uploaded image.
    
    How It Works:
    1. Receives the image
    2. Extracts text with OCR
    3. Creates a conversation
    4. Saves the text
    5. Returns the text
    """
    
    # Check the file type
    allowed_types = ["image/png", "image/jpeg", "image/jpg", "image/bmp", "image/tiff"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Use: PNG, JPG, BMP, TIFF"
        )
    
    try:
        # Read the image
        image_bytes = await file.read()
        
        # Extract text
        result = extract_text_from_image_bytes(image_bytes)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        # Create a conversation
        conversation = create_conversation(
            db,
            current_user,
            f"📷 Image: {file.filename}"
        )
        
        # Save the text
        message = MessageCreate(
            role="assistant",
            content=f"📷 Extracted text from '{file.filename}':\n\n{result['text'][:500]}..."
        )
        add_message(db, conversation.id, message)
        
        return {
            "success": True,
            "text": result["text"],
            "conversation_id": conversation.id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))