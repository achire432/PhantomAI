"""
OCR SERVICE
============
Purpose: Extract text from images.

Why This Matters:
- Users have photos, screenshots, and scanned documents
- PhantomAI can read them
- Makes PhantomAI more capable

How It Works:
1. Takes an image
2. Uses Tesseract to read text
3. Returns the text

What Would Happen Without This:
- PhantomAI couldn't read images
- Users would have to type text manually
- Lost productivity
"""

import pytesseract
from PIL import Image
import os

def extract_text_from_image_bytes(image_bytes: bytes) -> dict:
    """
    Extract text from image bytes.
    
    How It Works:
    1. Opens the image from bytes
    2. Uses pytesseract to read text
    3. Returns the extracted text
    
    What You'll See:
    - Success: {"success": True, "text": "Hello world"}
    - Failure: {"success": False, "error": "..."}
    """
    try:
        # Open image from bytes
        from io import BytesIO
        image = Image.open(BytesIO(image_bytes))
        
        # Extract text
        text = pytesseract.image_to_string(image, lang='eng')
        
        return {
            "success": True,
            "text": text.strip()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }