import os
import time
import pyttsx3
import speech_recognition as sr
import eel
import backend.feature as feature 

engine = pyttsx3.init('sapi5')

def speak(text):
    """Converts text to speech using pyttsx3 and sets a female voice."""
    text = str(text) 
    voices = engine.getProperty('voices')
    
    found_female = False
    
    # 1. Try to find a female voice by checking properties
    for voice in voices:
        # Check commonly used female voices (may need adjustment based on system language)
        if "zira" in voice.name.lower() or "eva" in voice.name.lower() or voice.gender == 'female':
            engine.setProperty('voice', voice.id)
            found_female = True
            break
            
    # 2. If no female voice is explicitly found, try Index 1 or Index 0 as a fallback
    if not found_female:
        if len(voices) > 1:
            # Try index 1 as a common fallback for female voice
            engine.setProperty('voice', voices[1].id) 
            print("Warning: Could not find explicit female voice, defaulting to index 1.")
        elif len(voices) > 0:
            # Fallback to the first available voice
            engine.setProperty('voice', voices[0].id)
        else:
            print(f"ERROR: No TTS voices found on system. Cannot speak: {text}")
            return 
    
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait() 
    eel.receiverText(text)
def play_assistant_sound():
    """Plays the assistant ready sound. (Uses feature.py logic)"""
    feature.play_assistant_sound()
        
def takecommand():
    """Captures voice input from the microphone."""
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("I'm listening...")
            eel.DisplayMessage("I'm listening...")
            r.pause_threshold = 1
            print("Adjusting for ambient noise for 1 second...")
            # Increased duration for better noise adjustment
            r.adjust_for_ambient_noise(source, duration=1.5) 
            
            audio = r.listen(source, timeout=5, phrase_time_limit=8) 
            
    except Exception as e:
        print(f"Microphone Access/Listening Error: {str(e)}")
        eel.DisplayMessage(f"Microphone Error: {str(e)}")
        return "" 
        
    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}\n")
        eel.DisplayMessage(query)
        return query.lower()
        
    except sr.UnknownValueError:
        print("Sorry, I did not catch that.")
        eel.DisplayMessage("Sorry, I did not catch that.")
        return "" 
    except Exception as e:
        print(f"Google Recognition Error: {str(e)}\n")
        eel.DisplayMessage(f"Recognition Error: {str(e)}")
        return ""

@eel.expose
def takeAllCommands(message=None):
    query = None
    confirmation_message = None 
    
    # 1. Get the command (voice or typed)
    if message is None:
        query = takecommand()
        if not query:
            return "No voice input received." 
        eel.senderText(query)
    else:
        query = message.lower()
        eel.senderText(query)
        
    # 2. Process the command
    try:
        if query:
            # Command: Open Application
            if "open" in query:
                # Calls feature.openCommand which now RETURNS the message string
                confirmation_message = feature.openCommand(query) 
            
            # Command: YouTube
            elif "on youtube" in query:
                feature.PlayYoutube(query)
                confirmation_message = "Playing content on YouTube."
            
            # Command: General Conversation (Hello, What is, etc.)
            elif "hello" in query or "hey" in query or "tell me about" in query or "what is" in query: 
                
                if os.path.exists("backend/cookie.json"): 
                    # If chatbot file exists, use chatbot
                    feature.chatBot(query) 
                    confirmation_message = "Chatbot has responded."
                else:
                    # If chatbot file is missing, provide a default response
                    confirmation_message = "Hello, I am your assistant. How can I help you?"
            
            # Unrecognized command
            else:
                confirmation_message = "I don't know that command yet."
            
        else:
            confirmation_message = "No command was given."
            
        # 3. Speak final confirmation AFTER executing the command
        if confirmation_message and "Chatbot has responded." not in confirmation_message:
            speak(confirmation_message)
            
    except Exception as e:
        print(f"An error occurred during command execution: {e}")
        speak("Sorry, I encountered an internal error while executing your request.")
        eel.ShowHood()
        return f"Error executing command: {e}" 
        
    eel.ShowHood()
    return "Command processing completed."