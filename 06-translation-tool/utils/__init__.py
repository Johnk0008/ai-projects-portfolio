import pyperclip
from gtts import gTTS
import os
import tempfile
from playsound import playsound

def copy_to_clipboard(text):
    """Copy text to clipboard"""
    try:
        pyperclip.copy(text)
        return True
    except Exception as e:
        print(f"Error copying to clipboard: {e}")
        return False

def text_to_speech(text, lang='en'):
    """Convert text to speech and play it"""
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            temp_filename = temp_file.name
        
        # Save and play the audio
        tts.save(temp_filename)
        playsound(temp_filename)
        
        # Clean up
        os.unlink(temp_filename)
        return True
    except Exception as e:
        print(f"Error in text-to-speech: {e}")
        return False