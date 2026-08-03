"""
UPLOAD ROUTER
==============
Purpose: Handle file uploads from users.
"""

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import os

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.services.file_reader import extract_text
from backend.app.services.conversation import create_conversation, add_message
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
    try:
        # Save the file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Extract ALL text from the file
        text_content = extract_text(file_path)
        
        # Create a new conversation
        conversation = create_conversation(
            db,
            current_user,
            f"📄 File: {file.filename}"
        )
        
        # Store the FULL file content (not just preview!)
        message = MessageCreate(
            role="assistant",
            content=f"📄 FILE CONTENT: '{file.filename}'\n\n{text_content}\n\nYou can ask questions about this file."
        )
        add_message(db, conversation.id, message)
        
        return {
            "message": "File uploaded successfully!",
            "conversation_id": conversation.id,
            "file_name": file.filename,
            "content_length": len(text_content)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")