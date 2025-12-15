import cv2
from deepface import DeepFace
 ##import pywhatkit  # Library to control YouTube
import webbrowser
import time

# --- SETTINGS ---
# MUSIC_COOLDOWN: Time (in seconds) to wait before playing a new song.
# Set to 15 seconds for testing, or 300 (5 mins) for real use.
MUSIC_COOLDOWN = 15 

print("System Initializing... This might take a few seconds.")

# 1. Load Face Detection Tools
# OpenCV has a built-in face detector called Haar Cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 2. Open Webcam (0 is usually the default laptop camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Could not find a webcam.")
    exit()

# Variable to track the last time we played music
last_music_time = 0 

print("✅ AI Started! Look at the camera.")

while True:
    # 3. Read video frame by frame
    ret, frame = cap.read()
    if not ret:
        print("Error reading frame.")
        break

    # 4. Convert to Grayscale (Face detection works faster in B&W)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 5. Detect Faces
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Draw a green box around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Crop the face (Region of Interest)
        face_roi = frame[y:y+h, x:x+w]

        try:
            # 6. Analyze Emotion (The AI Part)
            # enforce_detection=False allows it to run even if the face is partially hidden
            result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
            
            # Get the top emotion (e.g., "happy", "sad")
            emotion = result[0]['dominant_emotion']
            
            # Display the emotion text on screen
            cv2.putText(frame, f"Mood: {emotion.upper()}", (x, y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # 7. The DJ Logic (Play Music)
            # We check if enough time has passed since the last song
            if time.time() - last_music_time > MUSIC_COOLDOWN:
                
                if emotion == 'sad':
                    print("Detected SADNESS... Playing uplifting music!")
                    pywhatkit.playonyt("Uplifting pop songs 2024") # Search query for YouTube
                    last_music_time = time.time() # Reset timer

                elif emotion == 'angry':
                    print("Detected ANGER... Playing calming sounds.")
                    pywhatkit.playonyt("Calming nature sounds water")
                    last_music_time = time.time()

                elif emotion == 'happy':
                    print("Detected HAPPINESS... Playing party music!")
                    pywhatkit.playonyt("Top party hits 2024")
                    last_music_time = time.time()
                
                # 'Neutral' mood does nothing, allowing you to focus.

        except Exception as e:
            # If the AI gets confused or face moves too fast, just skip this frame
            pass

    # 8. Show the video window
    cv2.imshow('Project 1: Mood DJ', frame)

    # Press 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()