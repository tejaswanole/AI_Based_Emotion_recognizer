import cv2
from deepface import DeepFace
import webbrowser  # Opens Spotify links
import time

# --- SETTINGS ---
MUSIC_COOLDOWN = 20  # Wait 20 seconds before changing the song again

# --- SPOTIFY PLAYLIST LINKS ---
# You can replace these links with your OWN favorite playlists later!
SPOTIFY_PLAYLISTS = {
    "happy": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC", # "Happy Hits"
    "sad": "https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1",   # "Sad Songs"
    "angry": "https://open.spotify.com/playlist/37i9dQZF1DWXe9gFZP0gtP", # "Stress Relief"
    "neutral": "", # Do nothing
    "surprise": "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M", # "Todays Top Hits"
    "fear": "https://open.spotify.com/playlist/37i9dQZF1DXaImRpG7HXqp",    # "Calming Acoustic"
    "disgust": "https://open.spotify.com/playlist/37i9dQZF1DXaImRpG7HXqp"
}

print("🎧 Spotify Mood DJ Initializing...")

# 1. Load Face Detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 2. Open Webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Could not find a webcam.")
    exit()

last_music_time = 0 

print("✅ AI Started! Look at the camera.")

while True:
    ret, frame = cap.read()
    if not ret: break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        face_roi = frame[y:y+h, x:x+w]

        try:
            # Analyze Emotion
            result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
            emotion = result[0]['dominant_emotion']
            
            # Display Mood
            cv2.putText(frame, f"Mood: {emotion.upper()}", (x, y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # --- DJ LOGIC (SPOTIFY EDITION) ---
            if time.time() - last_music_time > MUSIC_COOLDOWN:
                
                # Check if we have a playlist for this emotion
                if emotion in SPOTIFY_PLAYLISTS and SPOTIFY_PLAYLISTS[emotion] != "":
                    print(f"🎵 Detected {emotion.upper()}... Opening Spotify!")
                    
                    # Open the link
                    webbrowser.open(SPOTIFY_PLAYLISTS[emotion])
                    
                    last_music_time = time.time()
                
        except Exception as e:
            pass

    cv2.imshow('Spotify Mood DJ', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()