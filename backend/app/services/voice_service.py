"""
VOICE SERVICE
==============
Purpose: Let PhantomAI hear you and speak back.

Why This Matters:
- This is the JARVIS feature
- Hands-free interaction
- Feels like a real assistant

How It Works:
1. Speech-to-Text: Listens to microphone → Converts to text
2. Text-to-Speech: Converts text → Speaks it out loud
3. Wake Word: Listens for "Hey Phantom"

Libraries:
- speech_recognition: Hear and convert
- pyttsx3: Speak back
- pyaudio: Microphone access
"""

import speech_recognition as sr
import pyttsx3
import threading
import time

# Initialize the speech engine
engine = pyttsx3.init()

# Initialize the recognizer
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Wake word detection (simple version)
wake_word = "hey phantom"
is_listening = False
stop_wake_listener = False

def listen_for_wake_word():
    """
    Listen continuously for the wake word "Hey Phantom".
    
    How It Works:
    1. Listens to microphone
    2. Checks if "hey phantom" was said
    3. If detected, triggers PhantomAI
    
    Example:
        You: "Hey Phantom"
        PhantomAI: "Yes, sir?" (starts listening)
    """
    global is_listening
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎤 Listening for 'Hey Phantom'...")
        
        while not stop_wake_listener:
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                text = recognizer.recognize_google(audio).lower()
                print(f"Heard: {text}")
                
                if wake_word in text:
                    print("🔊 Wake word detected!")
                    is_listening = True
                    speak("Yes, sir?")
                    return "wake_detected"
                    
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except Exception as e:
                print(f"Error: {e}")
    
    return "stopped"

def listen_for_command():
    """
    Listen for a command after wake word is detected.
    
    How It Works:
    1. PhantomAI says "Yes, sir?"
    2. You speak your command
    3. Converts speech to text
    4. Returns the text
    
    Example:
        You: "What is the weather?"
        Returns: "what is the weather"
    """
    global is_listening
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎤 Listening for command...")
        
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)
            print(f"📝 Command heard: {text}")
            is_listening = False
            return text
            
        except sr.WaitTimeoutError:
            is_listening = False
            return "timeout"
        except sr.UnknownValueError:
            is_listening = False
            return "unknown"
        except Exception as e:
            is_listening = False
            return f"error: {str(e)}"

def speak(text: str):
    """
    Make PhantomAI speak out loud.
    
    How It Works:
    1. Takes text
    2. Uses text-to-speech engine
    3. Speaks it
    
    Example:
        speak("Hello, how can I help?")
        → PhantomAI says "Hello, how can I help?"
    """
    print(f"🗣️ Speaking: {text}")
    engine.say(text)
    engine.runAndWait()

def speak_async(text: str):
    """
    Speak without blocking (non-blocking).
    """
    thread = threading.Thread(target=speak, args=(text,))
    thread.start()

def text_to_speech(text: str) -> dict:
    """
    API-friendly text-to-speech.
    
    Returns:
    {
        "success": True,
        "text": text,
        "spoken": True
    }
    """
    try:
        speak(text)
        return {
            "success": True,
            "text": text,
            "spoken": True
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def speech_to_text() -> dict:
    """
    API-friendly speech-to-text.
    
    Returns:
    {
        "success": True,
        "text": "what is the weather"
    }
    """
    try:
        text = listen_for_command()
        if text == "timeout":
            return {
                "success": False,
                "error": "No speech detected (timeout)"
            }
        elif text == "unknown":
            return {
                "success": False,
                "error": "Could not understand speech"
            }
        elif text.startswith("error:"):
            return {
                "success": False,
                "error": text
            }
        else:
            return {
                "success": True,
                "text": text
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }