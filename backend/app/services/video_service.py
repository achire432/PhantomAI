"""
VIDEO SERVICE
==============
Purpose: Generate simple videos from text and images.
Uses moviepy (already installed).
"""

import os
import tempfile
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, concatenate_videoclips
import numpy as np
import base64
from io import BytesIO


def create_text_video(text: str, duration: int = 5, output_path: str = None) -> dict:
    """
    Create a simple video with text using moviepy.
    """
    try:
        temp_dir = tempfile.mkdtemp()
        output_path = output_path or os.path.join(temp_dir, "output.mp4")
        
        # Create frame with text
        frame = Image.new('RGB', (1920, 1080), color=(10, 10, 30))
        draw = ImageDraw.Draw(frame)
        
        # Load font
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 72)
            font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
        except:
            font = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Draw border
        draw.rectangle([50, 50, 1870, 1030], outline=(0, 200, 255), width=4)
        
        # Draw header
        draw.text((100, 100), "🧠 PHANTOM AI", fill=(0, 200, 255), font=font)
        
        # Wrap and draw text
        lines = []
        words = text.split()
        current_line = ""
        for word in words:
            if len(current_line) + len(word) < 35:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        
        y = 300
        for line in lines:
            draw.text((100, y), line, fill='white', font=font_small)
            y += 60
        
        # Draw footer
        draw.text((100, 950), "Achire Intelligent Systems", fill=(100, 100, 150), font=font_small)
        
        # Convert to numpy array for moviepy
        frame_array = np.array(frame)
        
        # Create video clip
        clip = ImageClip(frame_array, duration=duration)
        
        # Add fade in/out
        clip = clip.fadein(0.5).fadeout(0.5)
        
        # Write video
        clip.write_videofile(output_path, fps=24, verbose=False, logger=None)
        
        return {
            "success": True,
            "path": output_path,
            "duration": duration,
            "text": text
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def create_slideshow_video(images: list, duration_per_image: int = 3) -> dict:
    """
    Create a slideshow video from images using moviepy.
    """
    try:
        clips = []
        for img in images:
            if isinstance(img, str) and (img.startswith('data:image') or len(img) > 100):
                # Base64 image
                if 'base64,' in img:
                    img_data = img.split('base64,')[1]
                else:
                    img_data = img
                
                image_bytes = base64.b64decode(img_data)
                image = Image.open(BytesIO(image_bytes))
                temp_path = tempfile.mktemp(suffix=".png")
                image.save(temp_path)
                clip = ImageClip(temp_path, duration=duration_per_image)
            else:
                clip = ImageClip(img, duration=duration_per_image)
            
            clip = clip.fadein(0.3).fadeout(0.3)
            clips.append(clip)
        
        final_clip = concatenate_videoclips(clips, method="compose")
        
        output_path = tempfile.mktemp(suffix=".mp4")
        final_clip.write_videofile(output_path, fps=24, verbose=False, logger=None)
        
        return {
            "success": True,
            "path": output_path,
            "duration": len(images) * duration_per_image
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}