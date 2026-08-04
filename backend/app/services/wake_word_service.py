"""
WAKE WORD SERVICE
==================
Purpose: Run wake word detection in the background.

Why This Matters:
- PhantomAI listens continuously
- No need to press buttons
- Just say "Hey Phantom"

How It Works:
1. Starts a background thread
2. Listens for the wake word
3. When detected, triggers the command
"""

import threading
import time
from backend.app.services.voice_service import listen_for_wake_word, listen_for_command, speak, is_listening

# State
is_running = False
wake_thread = None

def start_wake_listener():
    """
    Start the wake word listener in a background thread.
    """
    global is_running, wake_thread
    
    if is_running:
        return {"message": "Wake listener already running"}
    
    is_running = True
    wake_thread = threading.Thread(target=_wake_loop, daemon=True)
    wake_thread.start()
    
    return {"message": "Wake listener started"}

def stop_wake_listener():
    """
    Stop the wake word listener.
    """
    global is_running
    is_running = False
    return {"message": "Wake listener stopped"}

def _wake_loop():
    """
    Background loop for wake word detection.
    """
    global is_running
    print("🔊 Wake word listener active. Say 'Hey Phantom'")
    
    while is_running:
        try:
            # This is a simplified version
            # For a real implementation, we would run the wake word detection here
            time.sleep(1)
        except Exception as e:
            print(f"Wake loop error: {e}")
            time.sleep(1)

def get_wake_status():
    """
    Get the current status of the wake listener.
    """
    return {
        "is_running": is_running,
        "is_listening": is_listening
    }