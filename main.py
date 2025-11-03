import os
import eel
import warnings
import time
import threading

# Filter the pkg_resources UserWarning from Pygame/setuptools
warnings.filterwarnings("ignore", category=UserWarning, message="pkg_resources is deprecated as an API")

from backend.auth import recoganize
from backend.command import speak, play_assistant_sound, takeAllCommands 

# --- CRITICAL FIX: Global Flag to prevent double initialization ---
is_initialized = False

def main_task():
    
    print("Voice command loop started...")
    
    while True:
        try:
            # Calls takeAllCommands which handles voice input and command processing
            # NOTE: Your logic here means it listens continuously.
            command_text = takeAllCommands() 
            print(f"Command processed: {command_text}")
            
            # Reduces CPU usage by pausing the loop slightly
            time.sleep(1) 
                
        except Exception as e:
            print(f"Error in command loop: {e}")
            break 


def start():
    
    global is_initialized # <-- Declare global variable usage
    eel.init("frontend") 
    
    @eel.expose
    def init():
        
        global is_initialized # <-- Use global variable
        
        # --- CRITICAL FIX 2: Only allow initialization ONCE ---
        if is_initialized:
            print("Initialization skipped (already run).")
            return "Initialization complete."
        
        is_initialized = True
        
        eel.hideLoader() 
        eel.DisplayMessage("Ready for Face Authentication...") 
        print("Starting Face Recognition...")
        
        # Check for Face Authentication success
        if recoganize.AuthenticateFace() == 1:
            
            eel.hideFaceAuth()      
            eel.hideFaceAuthSuccess() 
            
            speak("Face recognized successfully. Welcome to your assistant.")
            play_assistant_sound()      
            
            eel.hideStart() 
            
            # Start the continuous voice command loop in a separate thread
            threading.Thread(target=main_task).start()
            
            return "Authentication Successful" 
        else:
            
            # Authentication failed
            eel.DisplayMessage("Face not recognized. Please try again.")
            speak("Face not recognized. Please try again.")
            
            eel.showFaceAuth() 
            
            return "Authentication Failed"
            
    try:
        # Start the Eel server (using your preferred structure)
        eel.start("index.html", mode="edge", host="localhost", block=True)
    except Exception as e:
        print(f"Eel startup error: {e}")


if __name__ == '__main__':
    start()