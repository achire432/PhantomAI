from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from fastapi.responses import FileResponse

from pydantic import BaseModel

from backend.app.dependencies.auth import (
    get_current_user,
)

from backend.app.models.user import User

from backend.app.services.video_service import (
    create_text_video,
    create_slideshow_video,
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/video",
    tags=["Video"],
)


# ============================================================
# REQUEST MODELS
# ============================================================

class TextVideoRequest(BaseModel):

    text: str

    duration: int = 8

    aspect_ratio: str = "16:9"

    resolution: str = "720p"


class SlideshowRequest(BaseModel):

    images: list[str]

    duration_per_image: int = 3


# ============================================================
# TEXT -> AI VIDEO
# ============================================================

@router.post("/text")
def generate_text_video(
    request: TextVideoRequest,
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Generate a REAL AI video using Google Veo.
    """

    if not request.text.strip():

        raise HTTPException(
            status_code=400,
            detail="Video prompt cannot be empty.",
        )

    result = create_text_video(
        text=request.text,
        duration=request.duration,
        aspect_ratio=request.aspect_ratio,
        resolution=request.resolution,
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
            "phantom_ai_veo_video.mp4",
        ),
        headers={
            "X-Phantom-Tool": (
                "video_generation"
            ),
            "X-Phantom-Type": (
                "veo_ai_video"
            ),
            "X-Phantom-Provider": (
                "google-veo-3.1"
            ),
        },
    )


# ============================================================
# IMAGE -> SLIDESHOW
# ============================================================

@router.post("/slideshow")
def generate_slideshow(
    request: SlideshowRequest,
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Generate an MP4 slideshow
    from supplied images.
    """

    if not request.images:

        raise HTTPException(
            status_code=400,
            detail=(
                "At least one image "
                "is required."
            ),
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
            "X-Phantom-Tool": (
                "video_generation"
            ),
            "X-Phantom-Type": (
                "slideshow_video"
            ),
        },
    )
