import cv2
import winsound  # Built-in Windows tool for beeping
import time

# --- SETTINGS ---
# Number of consecutive frames with "No Eyes" before alarm triggers
# 30 frames = approx 1-2 seconds
DROWSINESS_THRESHOLD = 30 

print("✅ Focus Guardian Starting...")
print("ℹ️  Alerts: Visual (Red Screen) + Audio (Beep)")

# --- LOAD DETECTORS ---
# We use standard OpenCV detectors (Pre-installed)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

cap = cv2.VideoCapture(0)

# Counters
closed_eyes_frames = 0

print("✅ Active! Look at the camera. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret: break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 1. Detect Face
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Default status
    status = "Status: Awake"
    color = (0, 255, 0) # Green
    
    # Reset counter if no face is found (prevents false alarms when you leave desk)
    if len(faces) == 0:
        closed_eyes_frames = 0

    for (x, y, w, h) in faces:
        # Draw box around face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 1)
        
        # 2. Look for Eyes INSIDE the face region
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        # Detect eyes
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 4)
        
        # 3. Logic: Face is there, but eyes are MISSING? -> Likely Sleeping
        if len(eyes) == 0:
            closed_eyes_frames += 1
            status = "Status: SLEEPING?"
            color = (0, 0, 255) # Red
        else:
            closed_eyes_frames = 0
            status = "Status: Awake"
            color = (0, 255, 0) # Green
            
            # Draw green boxes around eyes to show we see them
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    # 4. Trigger Alarm (Visual + Sound)
    if closed_eyes_frames > DROWSINESS_THRESHOLD:
        # A. Visual Alert: Big Text
        cv2.putText(frame, "WAKE UP!", (50, 200), 
                    cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)
        
        # B. Visual Alert: Red Border
        cv2.rectangle(frame, (0,0), (frame.shape[1], frame.shape[0]), (0,0,255), 20)
        
        # C. Audio Alert: Beep
        # Frequency = 1000Hz, Duration = 100ms
        # We use a short duration so video doesn't freeze
        winsound.Beep(1000, 100) 
    
    # Display Status Text
    cv2.putText(frame, status, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow('Project 2: Focus Guardian', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()