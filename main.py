import numpy as np
import json
import cv2

with open('user_config.ini') as infile:
    user_config = json.load(infile)
    video_path = user_config['source_video_path']

cap = cv2.VideoCapture(video_path)
ret, firstframe = cap.read()

#Array to store positions
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
positions = -np.ones((length,2)) #(x,y) array
#positions = -np.ones((length,3)) #(x,y,size) array


#Run all filters on first image
t=0
firstgray  = cv2.cvtColor(firstframe, cv2.COLOR_BGR2GRAY)
firstfilt1 = cv2.bilateralFilter(firstgray,7,75,75)
firstfilt2 = cv2.medianBlur(firstfilt1,7)
ret, firstthresh = cv2.threshold(firstfilt2,127,255,cv2.THRESH_BINARY)
firstedges = cv2.Canny(firstthresh,75,75)

#Loop over video
while(cap.isOpened() and t<length-10):
    ret, frame = cap.read()
    t=t+1

    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('gray',gray)
    
    frame = cv2.medianBlur(gray,5)
    #cv2.imshow('medianBlur',frame)
    
    frame = cv2.bilateralFilter(frame,7,75,75)
    #cv2.imshow('bfilter',frame)
    #filt2 = cv2.GaussianBlur(frame,(5,5),2)
    
    ret, thresh = cv2.threshold(frame,127,255,cv2.THRESH_BINARY)
    #cv2.imshow('thresh',thresh)

    #laplacian = cv2.Laplacian(denoise,cv2.CV_64F)
    edges = cv2.Canny(thresh,75,75)
    #cv2.imshow('edges',edges)
    
    threshdiff = firstthresh - thresh
    #threshdiff = cv2.absdiff(firstthresh, frame)
    #cv2.imshow('threshdiff',threshdiff)
    
    threshdiffblur = cv2.medianBlur(threshdiff,5)
    ret, threshdiffblur = cv2.threshold(threshdiffblur,127,255,cv2.THRESH_BINARY)
    cv2.imshow('fly_silhouette',threshdiffblur)
   
    try:
        img,contours,hierarchy = cv2.findContours(threshdiffblur, 1, 2)
        contours = sorted(contours,key=cv2.contourArea, reverse=True)
        cnt = contours[0]

        (x,y),radius = cv2.minEnclosingCircle(cnt)
        center = (int(x),int(y))
        radius = int(radius)

        cv2.circle(gray,center,radius,(0,255,0),2)
        cv2.imshow('flyingray',gray)

        positions[t] = (x,y)
        print('\rWe are now in good t={}\r'.format(t), end='')
    except Exception as e:
    	print(e, '\rWe are now in bad  t={}\r'.format(t), end='')
    	pass
   		#raise e


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

np.savetxt('positions.txt',positions)
print ('exported location data')
cap.release()
cv2.destroyAllWindows()

