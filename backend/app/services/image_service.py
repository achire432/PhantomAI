"""
IMAGE SERVICE
==============
Purpose: Generate images from text descriptions.

Why This Matters:
- Users can create visual content
- PhantomAI can illustrate concepts
- Creative and fun feature

How It Works:
1. User provides a text description
2. Sends to Stability AI (free tier)
3. Returns the generated image

What Would Happen Without This:
- No visual creation capability
- Text-only assistant
- Less creative

Libraries:
- requests: For API calls
- pillow: For image processing (optional)

Stability AI API Notes:
- Free tier gives ~25 free generations
- v2 endpoint: api.stability.ai/v2beta/stable-image/generate/ultra
- v1 endpoint: api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image
"""

import os
import base64
import requests
import logging
from io import BytesIO
from PIL import Image

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Read API key from environment
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")


def generate_image_stability(prompt: str, height: int = 1024, width: int = 1024) -> dict:
    """
    Generate an image using Stability AI (Stable Diffusion).
    
    How It Works:
    1. Sends prompt to Stability AI API
    2. Returns base64 encoded image
    
    Returns:
    {
        "success": True,
        "image": "base64_encoded_image",
        "prompt": prompt
    }
    """
    
    # Check if API key exists
    logger.info(f"🔑 STABILITY_API_KEY exists: {bool(STABILITY_API_KEY)}")
    
    if not STABILITY_API_KEY:
        return {
            "success": False, 
            "error": "STABILITY_API_KEY not set. Please add to .env.\n\nGet your free key at: https://platform.stability.ai"
        }
    
    # Log safely (never print full key)
    logger.info(f"🔑 API Key length: {len(STABILITY_API_KEY)} characters")
    logger.info(f"🔑 API Key prefix: {STABILITY_API_KEY[:10]}...")
    
    try:
        # ============================================
        # Try v2 endpoint first (NEWER API)
        # ============================================
        url_v2 = "https://api.stability.ai/v2beta/stable-image/generate/ultra"
        logger.info(f"🌐 Attempting v2 endpoint: {url_v2}")
        
        payload_v2 = {
            "prompt": prompt,
            "output_format": "png"
        }
        
        headers = {
            "Authorization": f"Bearer {STABILITY_API_KEY}",
            "Content-Type": "application/json",
        }
        
        response = requests.post(url_v2, json=payload_v2, headers=headers, timeout=60)
        
        logger.info(f"📊 v2 Status Code: {response.status_code}")
        
        # If v2 works, return the result
        if response.status_code == 200:
            logger.info("✅ v2 endpoint succeeded!")
            image_base64 = base64.b64encode(response.content).decode('utf-8')
            return {
                "success": True,
                "image": image_base64,
                "prompt": prompt,
                "format": "base64",
                "provider": "stability-v2"
            }
        
        # Log v2 error for debugging
        try:
            error_data = response.json()
            logger.error(f"❌ v2 Error Response: {error_data}")
        except:
            logger.error(f"❌ v2 Error Text: {response.text[:500]}")
        
        # ============================================
        # Fallback to v1 endpoint (OLDER API)
        # ============================================
        logger.info("🔄 Falling back to v1 endpoint...")
        url_v1 = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        
        payload_v1 = {
            "text_prompts": [{"text": prompt, "weight": 1}],
            "cfg_scale": 7,
            "height": height,
            "width": width,
            "samples": 1,
            "steps": 30,
        }
        
        response = requests.post(url_v1, json=payload_v1, headers=headers, timeout=60)
        
        logger.info(f"📊 v1 Status Code: {response.status_code}")
        
        # Handle different error codes for v1
        if response.status_code == 401:
            return {
                "success": False,
                "error": "Invalid Stability AI API key. Please check your STABILITY_API_KEY in .env"
            }
        
        if response.status_code == 429:
            return {
                "success": False,
                "error": "Rate limit exceeded. Your free tier may be exhausted. Please wait or upgrade."
            }
        
        if response.status_code == 400:
            # Try to get the actual error from Stability AI
            try:
                error_data = response.json()
                logger.error(f"❌ v1 Error Response: {error_data}")
                return {
                    "success": False,
                    "error": f"Stability API Error: {error_data}"
                }
            except:
                return {
                    "success": False,
                    "error": f"Stability API Error (400): {response.text[:200]}"
                }
        
        response.raise_for_status()
        
        # Get the image from the response
        data = response.json()
        image_base64 = data["artifacts"][0]["base64"]
        
        return {
            "success": True,
            "image": image_base64,
            "prompt": prompt,
            "format": "base64",
            "provider": "stability-v1"
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Request Exception: {str(e)}")
        return {"success": False, "error": f"Request failed: {str(e)}"}
    except Exception as e:
        logger.error(f"❌ Unexpected Exception: {str(e)}")
        return {"success": False, "error": str(e)}


def generate_image(prompt: str, provider: str = "stability") -> dict:
    """
    Generate an image using the specified provider.
    
    Currently supports:
    - stability: Stability AI (free tier)
    - dalle: OpenAI DALL-E (requires OpenAI API key)
    """
    if provider == "stability":
        return generate_image_stability(prompt)
    elif provider == "dalle":
        return {"success": False, "error": "DALL-E support requires OpenAI API key"}
    else:
        return {"success": False, "error": f"Unknown provider: {provider}"}


def decode_image_to_file(base64_image: str, output_path: str) -> dict:
    """
    Decode a base64 image and save it to a file.
    """
    try:
        image_data = base64.b64decode(base64_image)
        with open(output_path, 'wb') as f:
            f.write(image_data)
        return {"success": True, "path": output_path}
    except Exception as e:
        return {"success": False, "error": str(e)}


def display_image(base64_image: str):
    """
    Display a base64 image (for testing).
    """
    try:
        image_data = base64.b64decode(base64_image)
        image = Image.open(BytesIO(image_data))
        image.show()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}