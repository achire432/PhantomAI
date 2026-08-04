"""
APP LAUNCHER SERVICE
=====================
Purpose: Launch applications on your computer.

Why This Matters:
- Real JARVIS-like experience
- Open apps without clicking
- Faster workflow

How It Works:
- Uses subprocess to open apps
- Works on macOS (open command)
- Safe and controlled
"""

import subprocess
import os

def launch_app(app_name: str) -> dict:
    """
    Launch an application.
    
    How It Works:
    - On macOS: uses 'open -a "App Name"'
    - On Windows: uses 'start "App Name"'
    
    Returns:
    {
        "success": True,
        "app": "VS Code"
    }
    """
    try:
        # MacOS
        subprocess.run(['open', '-a', app_name], check=True)
        
        return {
            "success": True,
            "app": app_name
        }
        
    except subprocess.CalledProcessError:
        # App not found
        return {
            "success": False,
            "error": f"App '{app_name}' not found"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def list_common_apps() -> list:
    """
    List common applications on the system.
    """
    common_apps = [
        "VS Code",
        "Chrome",
        "Firefox",
        "Safari",
        "Terminal",
        "Finder",
        "Spotify",
        "Slack",
        "Discord",
        "Postman",
        "Docker",
        "PyCharm"
    ]
    return common_apps