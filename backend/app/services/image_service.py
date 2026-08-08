import os
import base64
import logging
from io import BytesIO
from typing import Optional

import requests
from PIL import Image

logger = logging.getLogger(__name__)


STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")


# ============================================================
# STABILITY AI
# ============================================================

def generate_image_stability(
    prompt: str,
    aspect_ratio: str = "1:1",
) -> dict:
    """
    Generate an image using Stability AI.

    Uses multipart/form-data as required by the
    Stability AI stable-image API.
    """

    api_key = os.getenv("STABILITY_API_KEY")

    if not api_key:
        return {
            "success": False,
            "error": (
                "STABILITY_API_KEY is not configured. "
                "Add it to your .env file and restart the backend."
            ),
        }

    if not prompt or not prompt.strip():
        return {
            "success": False,
            "error": "Image prompt cannot be empty.",
        }

    url = (
        "https://api.stability.ai/"
        "v2beta/stable-image/generate/ultra"
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "image/*",
    }

    # IMPORTANT:
    #
    # Stability expects multipart/form-data.
    #
    # Do NOT use:
    #
    # json=payload
    #
    # because that sends application/json.
    #
    # data=payload causes requests to create the
    # multipart/form-data request when combined with files.

    data = {
        "prompt": prompt.strip(),
        "output_format": "png",
        "aspect_ratio": aspect_ratio,
    }

    try:
        logger.info("Sending image request to Stability AI")

        response = requests.post(
            url,
            headers=headers,
            data=data,
            files={
                "none": (
                    None,
                    "",
                    "application/octet-stream",
                )
            },
            timeout=120,
        )

        logger.info(
            "Stability response status: %s",
            response.status_code,
        )

        if response.status_code == 200:
            image_base64 = base64.b64encode(
                response.content
            ).decode("utf-8")

            return {
                "success": True,
                "image": image_base64,
                "prompt": prompt,
                "format": "base64",
                "provider": "stability",
            }

        # ----------------------------------------------------
        # ERROR HANDLING
        # ----------------------------------------------------

        try:
            error_data = response.json()
        except Exception:
            error_data = response.text[:1000]

        logger.error(
            "Stability AI error: %s",
            error_data,
        )

        if response.status_code == 400:
            return {
                "success": False,
                "error": (
                    f"Stability AI rejected the request: "
                    f"{error_data}"
                ),
            }

        if response.status_code == 401:
            return {
                "success": False,
                "error": (
                    "Stability AI API key is invalid "
                    "or unauthorized."
                ),
            }

        if response.status_code == 402:
            return {
                "success": False,
                "error": (
                    "Stability AI requires available "
                    "credits for this generation."
                ),
            }

        if response.status_code == 403:
            return {
                "success": False,
                "error": (
                    "Stability AI denied this request. "
                    "Check your account/API permissions."
                ),
            }

        if response.status_code == 429:
            return {
                "success": False,
                "error": (
                    "Stability AI rate limit reached. "
                    "Please wait and try again."
                ),
            }

        return {
            "success": False,
            "error": (
                f"Stability AI returned HTTP "
                f"{response.status_code}: "
                f"{error_data}"
            ),
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": (
                "Stability AI request timed out."
            ),
        }

    except requests.exceptions.RequestException as error:
        logger.exception(
            "Stability AI request failed"
        )

        return {
            "success": False,
            "error": (
                f"Stability AI request failed: {error}"
            ),
        }

    except Exception as error:
        logger.exception(
            "Unexpected image generation error"
        )

        return {
            "success": False,
            "error": str(error),
        }


# ============================================================
# OPENAI IMAGE GENERATION
# ============================================================

def generate_image_openai(
    prompt: str,
) -> dict:
    """
    Generate an image through OpenAI.

    This is kept separate from Stability so PhantomAI
    can support multiple image providers later.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return {
            "success": False,
            "error": (
                "OPENAI_API_KEY is not configured."
            ),
        }

    try:
        from openai import OpenAI

        client = OpenAI(
            api_key=api_key
        )

        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024",
        )

        if not result.data:
            return {
                "success": False,
                "error": (
                    "OpenAI returned no image."
                ),
            }

        image_data = result.data[0]

        # OpenAI can return base64 image data.
        if getattr(
            image_data,
            "b64_json",
            None,
        ):
            return {
                "success": True,
                "image": image_data.b64_json,
                "prompt": prompt,
                "format": "base64",
                "provider": "openai",
            }

        # Some responses may provide a URL.
        if getattr(
            image_data,
            "url",
            None,
        ):
            return {
                "success": True,
                "image": image_data.url,
                "prompt": prompt,
                "format": "url",
                "provider": "openai",
            }

        return {
            "success": False,
            "error": (
                "OpenAI returned an unsupported "
                "image response format."
            ),
        }

    except ImportError:
        return {
            "success": False,
            "error": (
                "OpenAI Python package is not installed."
            ),
        }

    except Exception as error:
        logger.exception(
            "OpenAI image generation failed"
        )

        return {
            "success": False,
            "error": str(error),
        }


# ============================================================
# MAIN IMAGE ROUTER
# ============================================================

def generate_image(
    prompt: str,
    provider: str = "stability",
    aspect_ratio: str = "1:1",
) -> dict:
    """
    Main image generation service.

    Provider names:

        stability
        openai

    Future providers can be added here without changing
    the frontend architecture.
    """

    provider = (
        provider or "stability"
    ).strip().lower()

    if provider == "stability":
        return generate_image_stability(
            prompt=prompt,
            aspect_ratio=aspect_ratio,
        )

    if provider in {
        "openai",
        "dalle",
    }:
        return generate_image_openai(
            prompt=prompt,
        )

    return {
        "success": False,
        "error": (
            f"Unsupported image provider: "
            f"{provider}"
        ),
    }


# ============================================================
# BASE64 → FILE
# ============================================================

def decode_image_to_file(
    base64_image: str,
    output_path: str,
) -> dict:
    """
    Decode a base64 image and save it to disk.
    """

    try:
        image_data = base64.b64decode(
            base64_image
        )

        with open(
            output_path,
            "wb",
        ) as file:
            file.write(image_data)

        return {
            "success": True,
            "path": output_path,
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error),
        }


# ============================================================
# DISPLAY IMAGE
# ============================================================

def display_image(
    base64_image: str,
) -> dict:
    """
    Open a base64 image locally for testing.
    """

    try:
        image_data = base64.b64decode(
            base64_image
        )

        image = Image.open(
            BytesIO(image_data)
        )

        image.show()

        return {
            "success": True,
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error),
        }
