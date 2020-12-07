import cv2
import numpy as np
#install with pip install scikit-image
from skimage.measure import compare_ssim

import math

#get camera device
cap = cv2.VideoCapture(0)
'''
while True:
    ret,img=cap.read()
    cv2.imshow('img',img)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break
cv2.destroyAllWindows()

orb=cv2.ORB_create()

kp,des=orb.detectAndCompute(img,None)

imgWkp=cv2.drawKeypoints(img,kp,None)

cv2.imshow('img',img)
cv2.imshow('kp',imgWkp)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
global fgbg
fgbg = cv2.createBackgroundSubtractorMOG2(0,50)
kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
textOrg=(20,50)
x=0
while x<100:
    ret, frame = cap.read()
    x+=1
fingerCount=0
while True:
    ret, frame = cap.read()
    frame1 = frame[0:200,0:200]
    frame1=cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    frame1 = cv2.bilateralFilter(frame1,9,300,150)
    frame2 = cv2.GaussianBlur(frame1,(5,5),0)
    #frame2=cv2.fastNlMeansDenoisingColored(frame2,None,10,10,7,21)
    fgmask = fgbg.apply(frame2,learningRate=0)

    fgmask = cv2.morphologyEx(fgmask,cv2.MORPH_ERODE,kernel)
    #fgmask = cv2.morphologyEx(fgmask,cv2.MORPH_DILATE,kernel)

    fgmask= cv2.threshold(fgmask, 128, 255, cv2.THRESH_BINARY| cv2.THRESH_OTSU)[1]

    cnt, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnt)>0:
        cnt = max(cnt, key=lambda x: cv2.contourArea(x))
        cv2.drawContours(frame, [cnt], -1, (255,255,0), 2)
        #compute convex hull and find defects to find finger gaps
        hull = cv2.convexHull(cnt,returnPoints = False)
        try:
            defects = cv2.convexityDefects(cnt,hull)
        except:
            continue
        #sources: https://medium.com/analytics-vidhya/hand-detection-and-finger-counting-using-opencv-python-5b594704eb08
        #https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contours_more_functions/py_contours_more_functions.html
        if defects is not None:
            count=0
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                #draw hull
                cv2.line(frame,start,end,[0,255,0],2)
                #compute triangle from the contour
                a = np.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = np.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = np.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                angle = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
                #this step cleans up the small defects, since the finger gaps are
                #much larger than any other onesf
                if angle <= np.pi/2.25 and (b>50 or c>50):  # angle less than 90 degree, treat as finger gaps
                    count += 1
                    #draw fingers
                    cv2.line(frame,start,far,[255,0,0],2)
                    cv2.line(frame,far,end,[255,0,0],2)
                    #finger gap point
                    cv2.circle(frame, far, 4, [0, 0, 255], -1)
            if count > 0:
                count = count+1
            prevCount=fingerCount
            fingerCount=count
            cv2.putText(frame, str(fingerCount), textOrg,cv2.FONT_HERSHEY_SIMPLEX,1,[255,255,255])
    else:
        fingerCount=0
    cv2.imshow('mask',fgmask)
    cv2.imshow('frame',frame)
    cv2.imshow('frame2',frame2)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()
