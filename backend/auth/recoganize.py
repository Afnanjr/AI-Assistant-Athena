import cv2
import face_recognition
import os
import numpy as np
import time 

# Define the path where face images are stored
FACES_DIR = "assets/faces" 

def load_face_data():
    """Loads known faces and encodings from the specified directory."""
    known_face_encodings = []
    known_face_names = []
    
    if not os.path.exists(FACES_DIR) or not os.listdir(FACES_DIR):
        print(f"Error: No face images found in {FACES_DIR}.")
        return known_face_encodings, known_face_names

    for file_name in os.listdir(FACES_DIR):
        if file_name.endswith(('.jpg', '.jpeg', '.png')):
            path = os.path.join(FACES_DIR, file_name)
            try:
                image = face_recognition.load_image_file(path)
                face_encoding = face_recognition.face_encodings(image)
                
                if face_encoding:
                    known_face_encodings.append(face_encoding[0])
                    # Note: We still load the name here, but won't display it later
                    name = os.path.splitext(file_name)[0]
                    known_face_names.append(name)
                    print(f"Loaded face: {name}")
            except Exception as e:
                print(f"Warning: Could not load or process face image {file_name}: {e}")

    return known_face_encodings, known_face_names

# ... (get_working_camera function remains UNCHANGED) ...
def get_working_camera():
    """Tries to find the correct camera index by prioritizing standard indices 0 and 1."""
    
    # CRITICAL FIX: Prioritize index 0 and 1, as these are most common for real webcams.
    # We will try 0, then 1, then 2.
    for index in [0, 1, 2]: 
        # Use cv2.CAP_DSHOW for better Windows compatibility
        video_capture = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        
        # Give the OS time to initialize the camera hardware
        time.sleep(1) 
        
        if video_capture.isOpened():
            # Check if it returns a valid frame (to ensure it's not a dummy/locked camera)
            ret, frame = video_capture.read()
            if ret:
                print(f"Found working camera at index {index}")
                return video_capture
            else:
                # If it opens but returns no frame, release and try next
                video_capture.release()
        
    return None

def AuthenticateFace():
    """Captures video and attempts to authenticate the user's face."""
    
    known_face_encodings, known_face_names = load_face_data()
    
    if not known_face_encodings:
        print("Authentication failed: No known faces loaded.")
        return 0 

    video_capture = get_working_camera()
    
    if video_capture is None:
        print("Error: Could not open any real webcam. Check system settings or unplug virtual camera.")
        return 0

    print("Camera active. Looking for known face...")
    authenticated = False
    
    try:
        while video_capture.isOpened():
            ret, frame = video_capture.read()
            if not ret:
                break

            # Face recognition logic (scaled down)
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            
            
            for face_location, face_encoding in zip(face_locations, face_encodings):
                
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                
                # --- We ONLY use a status variable, completely ignoring known_face_names ---
                status_text = "Unknown" 
                
                if True in matches:
                    authenticated = True
                    # Set the text to display below the face
                    status_text = "Access Granted" 
                    
                # Scale back up face locations for drawing
                top, right, bottom, left = [coord * 4 for coord in face_location]

                # Draw a box around the face
                box_color = (0, 0, 255) if status_text == "Unknown" else (0, 255, 0)
                cv2.rectangle(frame, (left, top), (right, bottom), box_color, 2)

                # Draw a label with the status below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), box_color, cv2.FILLED)
                
                # --- FINAL FIX: Display the status text (Access Granted or Unknown) ---
                cv2.putText(frame, status_text, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)


            # Display frame with authentication status (Main text at top left)
            display_text = "Authenticating..." if not authenticated else "Authentication Successful!"
            color = (0, 255, 255) if not authenticated else (0, 255, 0)
            cv2.putText(frame, display_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            
            cv2.imshow('Face Authentication', frame)
            
            if authenticated:
                cv2.waitKey(2000) 
                break

            # Allow manual stop by pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"An error occurred during video capture: {e}")
    finally:
        if 'video_capture' in locals() and video_capture is not None:
             video_capture.release()
        cv2.destroyAllWindows()
        
    return 1 if authenticated else 0