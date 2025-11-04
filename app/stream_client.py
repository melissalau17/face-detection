# app/stream_client.py
import os
import time
import cv2
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")
URL = f"{API_URL.rstrip('/')}/main"

cap = cv2.VideoCapture(0)

print(f"Sending frames to: {URL}")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read frame from webcam.")
        break

    _, jpg = cv2.imencode('.jpg', frame)

    try:
        resp = requests.post(
            URL,
            data=jpg.tobytes(),
            headers={'Content-Type': 'application/octet-stream'}
        )
        print("Status:", resp.status_code, resp.text)
    except requests.exceptions.RequestException as e:
        print("Error sending frame:", e)

    # Send ~5 FPS
    time.sleep(0.2)

cap.release()
cv2.destroyAllWindows()