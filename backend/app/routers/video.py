from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User

from backend.app.services.video_service import (
    create_text_video,
    create_slideshow_video,
)


router = APIRouter(
    prefix="/video",
    tags=["Video"],
)


class TextVideoRequest(BaseModel):
    text: str
    duration: int = 5


class SlideshowRequest(BaseModel):
    images: list[str]
    duration_per_image: int = 3


@router.post("/text")
def generate_text_video(
    request: TextVideoRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Generate an MP4 video from text.
    """

    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Video text cannot be empty.",
        )

    result = create_text_video(
        request.text,
        request.duration,
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=400,
            detail=result.get(
                "error",
                "Video generation failed.",
            ),
        )

    return FileResponse(
        result["path"],
        media_type="video/mp4",
        filename=result.get(
            "filename",
            "phantom_ai_video.mp4",
        ),
        headers={
            "X-Phantom-Tool": "video_generation",
            "X-Phantom-Type": "text_video",
        },
    )


@router.post("/slideshow")
def generate_slideshow(
    request: SlideshowRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Generate an MP4 slideshow from images.
    """

    if not request.images:
        raise HTTPException(
            status_code=400,
            detail="At least one image is required.",
        )

    result = create_slideshow_video(
        request.images,
        request.duration_per_image,
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=400,
            detail=result.get(
                "error",
                "Slideshow generation failed.",
            ),
        )

    return FileResponse(
        result["path"],
        media_type="video/mp4",
        filename=result.get(
            "filename",
            "phantom_ai_slideshow.mp4",
        ),
        headers={
            "X-Phantom-Tool": "video_generation",
            "X-Phantom-Type": "slideshow_video",
        },
    )
