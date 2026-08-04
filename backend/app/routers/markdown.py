"""
MARKDOWN ROUTER
================
Purpose: Handle markdown file uploads and processing.
"""
import markdown
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import os

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.services.markdown_service import process_markdown, extract_text_from_markdown
from backend.app.services.conversation import create_conversation, add_message
from backend.app.schemas.message import MessageCreate

router = APIRouter(prefix="/markdown", tags=["Markdown"])

@router.post("/")
async def process_markdown_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Process a markdown file."""
    
    # Check file type
    if not file.filename.endswith('.md'):
        raise HTTPException(
            status_code=400,
            detail="Only .md files are supported"
        )
    
    try:
        # Read the file content
        content = await file.read()
        content_str = content.decode('utf-8')
        
        # Process markdown
        html = markdown.markdown(content_str)
        
        # Create a conversation
        conversation = create_conversation(
            db,
            current_user,
            f"📝 Markdown: {file.filename}"
        )
        
        # Save the text
        message = MessageCreate(
            role="assistant",
            content=f"📝 Processed markdown file '{file.filename}':\n\n{content_str[:500]}..."
        )
        add_message(db, conversation.id, message)
        
        return {
            "success": True,
            "html": html,
            "raw": content_str,
            "conversation_id": conversation.id,
            "file_name": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))