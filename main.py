import numpy as np
import json
import cv2
with open('user_config.ini') as infile:
    user_config = json.load(infile)
    video_path = user_config['source_video_path']

cap = cv2.VideoCapture(video_path)

while(cap.isOpened()):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()