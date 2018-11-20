#Identify pupils. Based on beta 1

import numpy as np
import cv2
import time
import math 
from math import *
import multiprocessing
from multiprocessing import *
from vision import BASE_DIR
w = 640
h = 480
def pupil(image, queue, lock):
    try:
        global w
        global h
        data = {
            'cx' : None,
            'cy' : None,
            'radius' : None
        }
        frame = cv2.resize(image, (480,640))
        faces = cv2.CascadeClassifier(BASE_DIR + '/vision/api/haarcascade_eye.xml')
        detected = faces.detectMultiScale(frame, 1.3, 5)

        pupilFrame = frame
        pupilO = frame
        windowClose = np.ones((5,5),np.uint8)
        windowOpen = np.ones((2,2),np.uint8)
        windowErode = np.ones((2,2),np.uint8)

        for (x,y,w,h) in detected:
            cv2.rectangle(frame, (x,y), ((x+w),(y+h)), (0,0,255),1)	
            cv2.line(frame, (x,y), ((x+w,y+h)), (0,0,255),1)
            cv2.line(frame, (x+w,y), ((x,y+h)), (0,0,255),1)
            pupilFrame = cv2.equalizeHist(frame[int(y)+int((h*.25)):int((y+h)), x:int((x+w))])

            pupilO = pupilFrame
            ret, pupilFrame = cv2.threshold(pupilFrame,55,255,cv2.THRESH_BINARY)
            pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_CLOSE, windowClose)
            pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_ERODE, windowErode)
            pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_OPEN, windowOpen)

            threshold = cv2.inRange(pupilFrame,250,255)
            _,contours, hierarchy = cv2.findContours(threshold,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

            try:
                if(len(contours) >= 2):
                    #find biggest blob
                    maxArea = 0
                    MAindex = 0
                    distanceX = []
                    currentIndex = 0 
                    for cnt in contours:
                        area = cv2.contourArea(cnt)
                        center = cv2.moments(cnt)
                        cx,cy = int(center['m10']/center['m00']), int(center['m01']/center['m00'])
                        distanceX.append(cx)
                        if area > maxArea:
                            maxArea = area
                            MAindex = currentIndex
                        currentIndex = currentIndex + 1
                    # print(cx, cy, area)
                    del contours[MAindex]
                    del distanceX[MAindex]
            except:
                pass

            eye = 'right'
            try:
                if(len(contours) >= 2):
                    if(eye == 'right'):
                        edgeOfEye = distanceX.index(min(distanceX))
                    else:
                        edgeOfEye = distanceX.index(max(distanceX))	
                    del contours[edgeOfEye]
                    del distanceX[edgeOfEye]

            except:
                pass

            try:
                if(len(contours) >= 1):
                    maxArea = 0
                    for cnt in contours:
                        area = cv2.contourArea(cnt)
                        if area > maxArea:
                            maxArea = area
                            largeBlob = cnt
            except:
                pass

            try:        
                if(len(largeBlob) > 0):	
                    center = cv2.moments(largeBlob)
                    cx,cy = int(center['m10']/center['m00']), int(center['m01']/center['m00'])
                    cv2.circle(pupilO,(cx,cy),5,255,-1)
            except:
                pass

            data = {
                'cx' : cx,
                'cy' : cy,
                'radius' : sqrt(area/math.pi)
            }
      
    except Exception as e:
        print(e)
        data = {
            'cx' : None,
            'cy' : None,
            'radius' : None
        }
    lock.acquire()
    queue.put(data)
    lock.release()
