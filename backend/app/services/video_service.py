import os
import tempfile
import base64
from io import BytesIO

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, concatenate_videoclips


def _wrap_text(text: str, max_chars: int = 42):
    """
    Wrap text into readable lines.
    """
    words = text.split()

    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= max_chars:
            current_line += word + " "
        else:
            if current_line:
                lines.append(current_line.strip())

            current_line = word + " "

    if current_line:
        lines.append(current_line.strip())

    return lines


def create_text_video(
    text: str,
    duration: int = 5,
    output_path: str | None = None,
) -> dict:
    """
    Create a simple MP4 video containing the supplied text.
    """

    try:
        text = text.strip()

        if not text:
            return {
                "success": False,
                "error": "Video text cannot be empty.",
            }

        duration = max(1, min(duration, 60))

        temp_dir = tempfile.mkdtemp()

        if output_path is None:
            output_path = os.path.join(
                temp_dir,
                "phantom_ai_text_video.mp4",
            )

        # ----------------------------------------------------
        # CREATE VIDEO FRAME
        # ----------------------------------------------------

        frame = Image.new(
            "RGB",
            (1920, 1080),
            color=(10, 10, 30),
        )

        draw = ImageDraw.Draw(frame)

        # ----------------------------------------------------
        # LOAD FONTS
        # ----------------------------------------------------

        try:
            font = ImageFont.truetype(
                "/System/Library/Fonts/Helvetica.ttc",
                72,
            )

            body_font = ImageFont.truetype(
                "/System/Library/Fonts/Helvetica.ttc",
                52,
            )

            footer_font = ImageFont.truetype(
                "/System/Library/Fonts/Helvetica.ttc",
                32,
            )

        except Exception:
            font = ImageFont.load_default()
            body_font = font
            footer_font = font

        # ----------------------------------------------------
        # BORDER
        # ----------------------------------------------------

        draw.rectangle(
            [50, 50, 1870, 1030],
            outline=(0, 200, 255),
            width=4,
        )

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        draw.text(
            (100, 100),
            "PHANTOM AI",
            fill=(0, 200, 255),
            font=font,
        )

        # ----------------------------------------------------
        # BODY TEXT
        # ----------------------------------------------------

        lines = _wrap_text(text)

        y = 330

        for line in lines:
            draw.text(
                (100, y),
                line,
                fill="white",
                font=body_font,
            )

            y += 75

            if y > 850:
                break

        # ----------------------------------------------------
        # FOOTER
        # ----------------------------------------------------

        draw.text(
            (100, 950),
            "Achire Intelligent Systems",
            fill=(100, 100, 150),
            font=footer_font,
        )

        # ----------------------------------------------------
        # CONVERT FRAME
        # ----------------------------------------------------

        frame_array = np.array(frame)

        clip = ImageClip(
            frame_array,
            duration=duration,
        )

        # ----------------------------------------------------
        # FADE EFFECT
        # ----------------------------------------------------

        clip = clip.fadein(0.5)
        clip = clip.fadeout(0.5)

        # ----------------------------------------------------
        # WRITE VIDEO
        # ----------------------------------------------------

        clip.write_videofile(
            output_path,
            fps=24,
            codec="libx264",
            audio=False,
            logger=None,
        )

        clip.close()

        return {
            "success": True,
            "path": output_path,
            "duration": duration,
            "text": text,
            "type": "text_video",
            "filename": "phantom_ai_text_video.mp4",
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error),
        }


def _decode_base64_image(image_data: str) -> Image.Image:
    """
    Convert base64/data URI into a PIL Image.
    """

    if image_data.startswith("data:image"):
        image_data = image_data.split(",", 1)[1]

    raw = base64.b64decode(image_data)

    image = Image.open(
        BytesIO(raw)
    ).convert("RGB")

    return image


def create_slideshow_video(
    images: list,
    duration_per_image: int = 3,
) -> dict:
    """
    Create an MP4 slideshow from base64 images.
    """

    temporary_files = []
    clips = []

    try:

        if not images:
            return {
                "success": False,
                "error": "At least one image is required.",
            }

        duration_per_image = max(
            1,
            min(duration_per_image, 30),
        )

        # ----------------------------------------------------
        # CREATE CLIPS
        # ----------------------------------------------------

        for image_data in images:

            if not isinstance(image_data, str):
                continue

            image = _decode_base64_image(
                image_data
            )

            # Standardize image size
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
                "error": "No valid images were supplied.",
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
            "duration": len(clips) * duration_per_image,
            "type": "slideshow_video",
            "image_count": len(clips),
            "filename": "phantom_ai_slideshow.mp4",
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
