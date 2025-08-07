import cv2
import numpy as np
import time
from datetime import datetime

# RTSP camera stream URIs using GStreamer pipeline
CAM1_URI = "rtspsrc location=rtsp://admin:Admin_123@192.168.1.188 latency=10 drop-on-latency=true ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
CAM2_URI = "rtspsrc location=rtsp://service:Admin_123@192.168.1.6 latency=10 drop-on-latency=true ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"

# Open the lag log file to record lag values
log_file = open("lag_log.txt", "a")

# Open camera streams using OpenCV with GStreamer backend
cap1 = cv2.VideoCapture(CAM1_URI, cv2.CAP_GSTREAMER)
cap2 = cv2.VideoCapture(CAM2_URI, cv2.CAP_GSTREAMER)

# Check if cameras opened successfully
if not cap1.isOpened() or not cap2.isOpened():
    print("Could not open one or both camera streams.")
    exit()

# Frame counters and timers for FPS calculation
count1, count2 = 0, 0
t1, t2 = time.time(), time.time()

while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not ret1 or not ret2:
        print("Failed to retrieve frames.")
        break

    count1 += 1
    count2 += 1

    # Calculate FPS
    fps1 = count1 / (time.time() - t1)
    fps2 = count2 / (time.time() - t2)

    # Simulated lag values (replace with actual timestamp difference if available)
    ts1 = time.time()
    ts2 = time.time()
    lag_diff_str = f"{abs(ts1 - ts2):.0f} ms"

    # Log lag difference to file
    log_line = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Lag: {lag_diff_str}\n"
    log_file.write(log_line)
    log_file.flush()

    # Overlay information on frames
    cv2.putText(frame1, f"FPS: {fps1:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(frame2, f"FPS: {fps2:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(frame1, f"Lag: {lag_diff_str}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
    cv2.putText(frame2, f"Lag: {lag_diff_str}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    # Show warning if lag exceeds threshold (example: 100 ms)
    lag_threshold_ms = 100
    if abs(ts1 - ts2) * 1000 > lag_threshold_ms:
        warning_text = "WARNING: High Lag Detected!"
        cv2.putText(frame1, warning_text, (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame2, warning_text, (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Display frames
    cv2.imshow('Camera 1', frame1)
    cv2.imshow('Camera 2', frame2)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap1.release()
cap2.release()
log_file.close()
cv2.destroyAllWindows()
