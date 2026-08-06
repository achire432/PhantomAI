"""
MARKDOWN ROUTER
================
Purpose: Handle markdown file uploads and processing.
"""

import os

import markdown

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
from backend.app.services.conversation import (
    create_conversation,
    add_message,
)
from backend.app.schemas.message import MessageCreate


router = APIRouter(
    prefix="/markdown",
    tags=["Markdown"]
)


@router.post("/")
async def process_markdown_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Process a Markdown file.

    The uploaded Markdown content is:
    1. Read
    2. Converted to HTML
    3. Stored in a conversation belonging to the user
    4. Returned to the client
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="File must have a filename."
        )

    # Check file extension safely
    filename = os.path.basename(file.filename)

    if not filename.lower().endswith(".md"):
        raise HTTPException(
            status_code=400,
            detail="Only .md files are supported."
        )

    try:
        # Read file
        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="The Markdown file is empty."
            )

        # Decode Markdown
        try:
            content_str = content.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="Markdown file must be UTF-8 encoded."
            )

        # Convert Markdown → HTML
        html = markdown.markdown(content_str)

        # Create conversation owned by current user
        conversation = create_conversation(
            db,
            current_user,
            f"📝 Markdown: {filename}"
        )

        # Store the full Markdown content
        message = MessageCreate(
            role="assistant",
            content=(
                f"📝 Processed markdown file '{filename}':\n\n"
                f"{content_str}"
            )
        )

        # Add to authorized conversation
        add_message(
            db,
            conversation,
            message
        )

        return {
            "success": True,
            "html": html,
            "raw": content_str,
            "conversation_id": conversation.id,
            "file_name": filename
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Markdown processing failed: {str(e)}"
        )

    finally:
        await file.close()
