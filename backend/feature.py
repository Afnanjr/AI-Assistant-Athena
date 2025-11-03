import subprocess
import os
import pywhatkit
import webbrowser
import eel
import time
import pygame
import threading # Added threading for sound playback
import backend.command as command 

# Define the sound path
ASSISTANT_SOUND_PATH = "frontend/assets/audio/start_sound.mp3"

# Initialize pygame mixer only once
try:
    if not pygame.mixer.get_init():
        pygame.mixer.init()
except pygame.error as e:
    print(f"Pygame Mixer Initialization Error: {e}")

def play_sound_thread():
    """Plays the sound in a separate thread to prevent blocking the main loop."""
    try:
        if pygame.mixer.get_init():
            if not os.path.exists(ASSISTANT_SOUND_PATH):
                print(f"ERROR: Sound file not found at {ASSISTANT_SOUND_PATH}")
                return

            pygame.mixer.music.load(ASSISTANT_SOUND_PATH)
            pygame.mixer.music.play()
            
            # Wait until the music finishes playing to ensure sound is heard
            while pygame.mixer.music.get_busy():
                time.sleep(0.1) 
    except Exception as e:
        print(f"Error playing sound: {e}")

def play_assistant_sound():
    """Starts a new thread to play the assistant ready sound."""
    # Ensure the sound plays without blocking the main thread
    threading.Thread(target=play_sound_thread).start()
        
def openCommand(query):
    """Opens applications based on user command and returns a status message."""
    
    query = query.lower()
    
    if "notebook" in query or "notepad" in query:
        subprocess.Popen(['notepad.exe'])
        return "Opening Notepad."
    
    elif "browser" in query or "chrome" in query:
        webbrowser.open("http://google.com")
        return "Opening web browser."

    elif "youtube" in query:
        webbrowser.open("http://youtube.com")
        return "Opening YouTube."
        
    elif "whatsapp" in query:
        try:
            subprocess.Popen(['whatsapp.exe'])
            return "Opening WhatsApp application."
        except FileNotFoundError:
            webbrowser.open("https://web.whatsapp.com/")
            return "Opening WhatsApp web."
            
    elif "calculator" in query:
        subprocess.Popen(['calc.exe'])
        return "Opening calculator."
    else:
        return "I don't know how to open that application."

def PlayYoutube(query):
    """Searches and plays videos on YouTube."""
    if "on youtube" in query:
        search_query = query.replace("on youtube", "").strip()
        pywhatkit.playonyt(search_query)

def chatBot(query):
    """Handles general conversational queries using the chatbot module."""
    # NOTE: The actual chatbot logic should be implemented here.
    command.speak("Getting answer from chatbot...")
    return "Chatbot logic executed."


def findContact(query):
    """Placeholder function to find contact details."""
    return "+911234567890", "Test Contact"

def whatsApp(Phone, message, flag, name):
    """Sends WhatsApp message or initiates call/video call."""
    if flag == 'message':
        pywhatkit.sendwhatmsg_instantly(Phone, message) 
    elif flag == 'call':
        pass
    elif flag == 'video call':
        pass