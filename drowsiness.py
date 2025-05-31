import cv2
import mediapipe as mp
from scipy.spatial import distance as dist
from threading import Thread
import numpy as np
import time
import pyttsx3

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)
draw_utils = mp.solutions.drawing_utils

EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 30
YAWN_THRESH = 15  # Adjusted threshold for better accuracy
alarm_status = False
alarm_status2 = False
saying = False
COUNTER = 0

# Eye indices for EAR (from MediaPipe)
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def alarm(msg):
    global alarm_status
    global alarm_status2
    global saying

    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed of speech

    if alarm_status or alarm_status2:
        print('call')
        saying = True
        engine.say(msg)
        engine.runAndWait()
        saying = False

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def lip_distance(landmarks, w, h):
    # Use center lip points for yawn detection
    top = int(landmarks[13].y * h)  # Upper inner lip center
    bottom = int(landmarks[14].y * h)  # Lower inner lip center
    return abs(top - bottom)

cap = cv2.VideoCapture(0)
time.sleep(1.0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:
            landmarks = face_landmarks.landmark

            # EAR Calculation
            left_eye = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in LEFT_EYE]
            right_eye = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in RIGHT_EYE]

            left_ear = eye_aspect_ratio(left_eye)
            right_ear = eye_aspect_ratio(right_eye)
            ear = (left_ear + right_ear) / 2.0

            for point in left_eye + right_eye:
                cv2.circle(frame, point, 2, (0, 255, 0), -1)

            # Lip Distance (Yawn Detection)
            lip_dist = lip_distance(landmarks, w, h)
            cv2.putText(frame, f"EAR: {ear:.2f}", (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, f"YAWN: {lip_dist:.2f}", (300, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # Optional: visualize lip points
            cv2.circle(frame, (int(landmarks[13].x * w), int(landmarks[13].y * h)), 3, (0, 255, 255), -1)
            cv2.circle(frame, (int(landmarks[14].x * w), int(landmarks[14].y * h)), 3, (255, 255, 0), -1)

            # Drowsiness Alert
            if ear < EYE_AR_THRESH:
                COUNTER += 1
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    if not alarm_status:
                        alarm_status = True
                        Thread(target=alarm, args=('Please open your eyes, you look sleepy',), daemon=True).start()
                    cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                COUNTER = 0
                alarm_status = False

            # Yawn Alert
            if lip_dist > YAWN_THRESH:
                cv2.putText(frame, "Yawn Alert", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                if not alarm_status2 and not saying:
                    alarm_status2 = True
                    Thread(target=alarm, args=('You are yawning. Take a short break.',), daemon=True).start()
            else:
                alarm_status2 = False

    cv2.imshow("Drowsiness Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
