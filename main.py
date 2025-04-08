import threading 
import pygame
import cv2
import imutils
import time
import os

# Load the alarm sound using pygame 
if not os.path.exists("alarm.wav"):
    print("Error: 'alarm.wav' not found in the current directory.")
    exit()

pygame.mixer.init()  # Initialize pygame mixer
alarm_sound = pygame.mixer.Sound("alarm.wav")

# Initialize the webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

# Alarm system flags 
alarm_mode = False
alarm_triggered = False
alarm_counter = 0

# Alarm function 
def beep_alarm():
    global alarm_triggered
    for _ in range(5):
        if not alarm_mode:
            break
        print("MOVEMENT DETECTED!")
        alarm_sound.play()  # Play sound using pygame
        time.sleep(1)
    time.sleep(5)  # Optional cooldown between alarms
    alarm_triggered = False

# Main loop 
while True:
    _, frame = cap.read()
    frame = imutils.resize(frame, width=500)

    if alarm_mode:
        # Preprocessing current frame
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

        # Motion detection
        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw

        # Sensitivity check
        if threshold.sum() > 10:
            alarm_counter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1

        cv2.imshow("Cam", threshold)
    else:
        cv2.imshow("Cam", frame)

    # Trigger the alarm if movement persists
    if alarm_counter > 20:
        if not alarm_triggered:
            alarm_triggered = True
            threading.Thread(target=beep_alarm).start()

    # Handle key presses
    key_pressed = cv2.waitKey(30)
    if key_pressed == ord("t"):
        alarm_mode = not alarm_mode
        alarm_counter = 0
        print("Alarm Mode ON" if alarm_mode else "Alarm Mode OFF")
    if key_pressed == ord("q"):
        alarm_mode = False
        break

cap.release()
cv2.destroyAllWindows()
