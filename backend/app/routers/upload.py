"""
UPLOAD ROUTER
==============
Purpose: Handle file uploads from users.
"""

import os

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
from backend.app.services.file_reader import extract_text
from backend.app.services.conversation import (
    create_conversation,
    add_message,
)
from backend.app.schemas.message import MessageCreate


router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/file")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a file, extract its text, and create a conversation
    containing the extracted content.
    """

    file_path = None

    try:
        # Make sure a filename exists
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="A file must have a filename."
            )

        # Prevent directory traversal from filenames
        safe_filename = os.path.basename(file.filename)

        file_path = os.path.join(
            UPLOAD_DIR,
            safe_filename
        )

        # Save the uploaded file
        content = await file.read()

        with open(file_path, "wb") as f:
            f.write(content)

        # Extract text
        text_content = extract_text(file_path)

        if text_content is None:
            text_content = ""

        # Create conversation owned by current user
        conversation = create_conversation(
            db,
            current_user,
            f"📄 File: {safe_filename}"
        )

        # Store extracted content
        message = MessageCreate(
            role="assistant",
            content=(
                f"📄 FILE CONTENT: '{safe_filename}'\n\n"
                f"{text_content}\n\n"
                "You can ask questions about this file."
            )
        )

        # IMPORTANT:
        # Pass the authorized conversation object
        add_message(
            db,
            conversation,
            message
        )

        return {
            "message": "File uploaded successfully!",
            "conversation_id": conversation.id,
            "file_name": safe_filename,
            "content_length": len(text_content)
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )

    finally:
        # Close UploadFile resources
        await file.close()
