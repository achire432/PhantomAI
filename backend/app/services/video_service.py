import os
import time
import tempfile
import base64
from io import BytesIO

from dotenv import load_dotenv
from PIL import Image

from google import genai
from google.genai import types


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

VEO_MODEL = "veo-3.1-generate-preview"


# ============================================================
# CLIENT
# ============================================================

def _get_client():
    """
    Create a Google Gemini Developer API client.
    """

    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Add GEMINI_API_KEY to the .env file."
        )

    return genai.Client(
        api_key=GEMINI_API_KEY
    )


# ============================================================
# TEXT -> REAL AI VIDEO
# ============================================================

def create_text_video(
    text: str,
    duration: int = 8,
    aspect_ratio: str = "16:9",
    resolution: str = "720p",
) -> dict:
    """
    Generate a real AI video using Google Veo 3.1.

    Veo 3.1 generates video with native audio.

    Supported durations:
        4
        6
        8 seconds

    Supported aspect ratios:
        16:9
        9:16

    Supported resolutions:
        720p
        1080p

    Returns:
        {
            "success": True,
            "path": "...",
            "filename": "...",
            "duration": 8,
            "provider": "google-veo-3.1"
        }
    """

    text = text.strip()

    if not text:
        return {
            "success": False,
            "error": "Video prompt cannot be empty.",
        }

    # --------------------------------------------------------
    # VALIDATE DURATION
    # --------------------------------------------------------

    allowed_durations = [4, 6, 8]

    if duration not in allowed_durations:
        return {
            "success": False,
            "error": (
                "Invalid duration. "
                "Veo 3.1 supports 4, 6, or 8 seconds."
            ),
        }

    # --------------------------------------------------------
    # VALIDATE ASPECT RATIO
    # --------------------------------------------------------

    if aspect_ratio not in ["16:9", "9:16"]:
        return {
            "success": False,
            "error": (
                "Aspect ratio must be "
                "16:9 or 9:16."
            ),
        }

    # --------------------------------------------------------
    # VALIDATE RESOLUTION
    # --------------------------------------------------------

    if resolution not in ["720p", "1080p"]:
        return {
            "success": False,
            "error": (
                "Resolution must be "
                "720p or 1080p."
            ),
        }

    # --------------------------------------------------------
    # 1080P CONSTRAINT
    # --------------------------------------------------------

    if resolution == "1080p" and duration != 8:
        return {
            "success": False,
            "error": (
                "1080p generation requires "
                "an 8-second video."
            ),
        }

    try:

        # ----------------------------------------------------
        # CREATE CLIENT
        # ----------------------------------------------------

        client = _get_client()

        print()
        print("=" * 60)
        print("PHANTOM AI — REAL VEO VIDEO GENERATION")
        print("=" * 60)
        print(f"Model:        {VEO_MODEL}")
        print(f"Duration:     {duration}s")
        print(f"Aspect Ratio: {aspect_ratio}")
        print(f"Resolution:   {resolution}")
        print("=" * 60)
        print("Sending request to Google Veo...")
        print()

        # ----------------------------------------------------
        # CONFIG
        #
        # IMPORTANT:
        # Do NOT use generate_audio=True here.
        #
        # Veo 3.1 already generates native audio.
        # ----------------------------------------------------

        config = types.GenerateVideosConfig(
            number_of_videos=1,
            duration_seconds=duration,
            aspect_ratio=aspect_ratio,
            resolution=resolution,
            )

        # ----------------------------------------------------
        # START GENERATION
        # ----------------------------------------------------

        operation = client.models.generate_videos(
            model=VEO_MODEL,
            prompt=text,
            config=config,
        )

        print("Veo generation started.")

        if getattr(operation, "name", None):
            print(
                f"Operation: {operation.name}"
            )

        # ----------------------------------------------------
        # WAIT FOR GENERATION
        # ----------------------------------------------------

        started_at = time.time()

        max_wait_seconds = 600

        while not operation.done:

            elapsed = int(
                time.time() - started_at
            )

            print(
                f"Waiting for Veo... "
                f"{elapsed}s elapsed"
            )

            if elapsed >= max_wait_seconds:

                return {
                    "success": False,
                    "error": (
                        "Video generation timed out "
                        "after 10 minutes."
                    ),
                }

            time.sleep(10)

            operation = client.operations.get(
                operation
            )

        print()
        print("Veo operation completed.")

        # ----------------------------------------------------
        # CHECK RESPONSE
        # ----------------------------------------------------

        if not operation.response:

            return {
                "success": False,
                "error": (
                    "Veo completed but returned "
                    "no response."
                ),
            }

        generated_videos = (
            operation.response.generated_videos
        )

        if not generated_videos:

            return {
                "success": False,
                "error": (
                    "Veo did not return "
                    "a generated video."
                ),
            }

        generated_video = generated_videos[0]

        video_file = generated_video.video

        if not video_file:

            return {
                "success": False,
                "error": (
                    "Veo returned an empty "
                    "video file."
                ),
            }

        # ----------------------------------------------------
        # LOCAL OUTPUT DIRECTORY
        # ----------------------------------------------------

        output_dir = os.path.join(
            tempfile.gettempdir(),
            "phantom_ai_videos",
        )

        os.makedirs(
            output_dir,
            exist_ok=True,
        )

        timestamp = int(time.time())

        output_path = os.path.join(
            output_dir,
            f"phantom_ai_veo_{timestamp}.mp4",
        )

        # ----------------------------------------------------
        # DOWNLOAD GENERATED VIDEO
        # ----------------------------------------------------

        print(
            "Downloading generated video..."
        )

        client.files.download(
            file=video_file
        )

        video_file.save(
            output_path
        )

        # ----------------------------------------------------
        # VERIFY FILE
        # ----------------------------------------------------

        if not os.path.exists(output_path):

            return {
                "success": False,
                "error": (
                    "Veo generated the video, "
                    "but the MP4 could not "
                    "be saved."
                ),
            }

        file_size = os.path.getsize(
            output_path
        )

        if file_size <= 0:

            return {
                "success": False,
                "error": (
                    "Generated video file "
                    "is empty."
                ),
            }

        print()
        print("=" * 60)
        print("VIDEO GENERATION SUCCESS")
        print("=" * 60)
        print(f"File: {output_path}")
        print(
            f"Size: "
            f"{file_size / 1024 / 1024:.2f} MB"
        )
        print("=" * 60)
        print()

        return {
            "success": True,
            "path": output_path,
            "filename": (
                "phantom_ai_veo_video.mp4"
            ),
            "duration": duration,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "provider": "google-veo-3.1",
            "prompt": text,
        }

    except Exception as error:

        error_message = str(error)

        print()
        print("=" * 60)
        print("VEO VIDEO GENERATION FAILED")
        print("=" * 60)
        print(error_message)
        print("=" * 60)

        return {
            "success": False,
            "error": (
                "Veo video generation failed: "
                f"{error_message}"
            ),
        }


# ============================================================
# BASE64 IMAGE DECODER
# ============================================================

def _decode_base64_image(
    image_data: str
) -> Image.Image:
    """
    Convert base64 image/data URI to PIL Image.
    """

    if image_data.startswith(
        "data:image"
    ):
        image_data = image_data.split(
            ",",
            1
        )[1]

    raw = base64.b64decode(
        image_data
    )

    return Image.open(
        BytesIO(raw)
    ).convert("RGB")


# ============================================================
# IMAGE -> SLIDESHOW VIDEO
# ============================================================

def create_slideshow_video(
    images: list,
    duration_per_image: int = 3,
) -> dict:
    """
    Create a local slideshow video from images.

    This is separate from Veo AI video generation.
    """

    if not images:

        return {
            "success": False,
            "error": (
                "At least one image is required."
            ),
        }

    duration_per_image = max(
        1,
        min(duration_per_image, 30),
    )

    temporary_files = []
    clips = []

    try:

        from moviepy.editor import (
            ImageClip,
            concatenate_videoclips,
        )

        # ----------------------------------------------------
        # CREATE IMAGE CLIPS
        # ----------------------------------------------------

        for image_data in images:

            if not isinstance(
                image_data,
                str
            ):
                continue

            image = _decode_base64_image(
                image_data
            )

            image = image.resize(
                (1920, 1080)
            )

            temp_file = tempfile.NamedTemporaryFile(
                suffix=".png",
                delete=False,
            )

            temp_file.close()

            image.save(
                temp_file.name,
                format="PNG",
            )

            temporary_files.append(
                temp_file.name
            )

            clip = ImageClip(
                temp_file.name,
                duration=duration_per_image,
            )

            clip = clip.fadein(0.3)
            clip = clip.fadeout(0.3)

            clips.append(clip)

        if not clips:

            return {
                "success": False,
                "error": (
                    "No valid images "
                    "were supplied."
                ),
            }

        # ----------------------------------------------------
        # JOIN CLIPS
        # ----------------------------------------------------

        final_clip = concatenate_videoclips(
            clips,
            method="compose",
        )

        output_path = tempfile.mktemp(
            suffix=".mp4"
        )

        final_clip.write_videofile(
            output_path,
            fps=24,
            codec="libx264",
            audio=False,
            logger=None,
        )

        final_clip.close()

        for clip in clips:
            clip.close()

        return {
            "success": True,
            "path": output_path,
            "duration": (
                len(clips)
                * duration_per_image
            ),
            "type": "slideshow_video",
            "image_count": len(clips),
            "filename": (
                "phantom_ai_slideshow.mp4"
            ),
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error),
        }

    finally:

        for path in temporary_files:

            try:

                if os.path.exists(path):
                    os.remove(path)

            except Exception:
                pass
