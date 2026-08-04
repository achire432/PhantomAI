"""
VIDEO ROUTER
=============
Purpose: Handle video generation API requests.

Endpoints:
- POST /video/text - Generate video from text
- POST /video/slideshow - Generate slideshow from images
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.services.video_service import create_text_video, create_slideshow_video

class TextVideoRequest(BaseModel):
    text: str
    duration: int = 5

class SlideshowRequest(BaseModel):
    images: List[str]
    duration_per_image: int = 3

router = APIRouter(prefix="/video", tags=["Video"])

@router.post("/text")
def generate_text_video(
    request: TextVideoRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate a video from text.
    
    Example:
        POST /video/text
        {"text": "Welcome to Phantom AI", "duration": 5}
    """
    result = create_text_video(request.text, request.duration)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return FileResponse(
        result["path"],
        media_type="video/mp4",
        filename="phantom_ai_video.mp4"
    )

@router.post("/slideshow")
def generate_slideshow(
    request: SlideshowRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate a slideshow video from images.
    
    Example:
        POST /video/slideshow
        {"images": ["base64_image1", "base64_image2"], "duration_per_image": 3}
    """
    result = create_slideshow_video(request.images, request.duration_per_image)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return FileResponse(
        result["path"],
        media_type="video/mp4",
        filename="slideshow.mp4"
    )