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
    filt1 = cv2.bilateralFilter(gray,7,75,75)
    filt2 = cv2.medianBlur(filt1,7)
    #gray = cv2.GaussianBlur(gray,(3,3),0)
    ret1, thresh = cv2.threshold(filt2,127,255,cv2.THRESH_BINARY)
    #laplacian = cv2.Laplacian(denoise,cv2.CV_64F)
    edges = cv2.Canny(thresh,75,75)

    cv2.imshow('frame',gray)
    cv2.imshow('frame1',edges)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()