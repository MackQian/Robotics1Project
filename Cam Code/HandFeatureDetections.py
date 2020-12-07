import cv2
import numpy as np
#install with pip install scikit-image
from skimage.measure import compare_ssim

import math

#get camera device
cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2(0,50)
kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
matcher=cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_BRUTEFORCE_HAMMING)
detect=cv2.AKAZE.create()
thresh=.2
textOrg=(20,50)
numGestures=5
x=0
while x<10:
    ret, frame = cap.read()
    x+=1

x=0
while x<10:
    ret, frame = cap.read()
    img= fgbg.apply(frame,learningRate=0)
    x+=1
#gather gestures
desList=[]
while len(desList)<numGestures:
    while True:
        ret,img=cap.read()
        cam=img
        img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img=cv2.bilateralFilter(img,9,300,150)
        img= cv2.GaussianBlur(img,(5,5),0)
        img= fgbg.apply(img,learningRate=0)
        img= cv2.morphologyEx(img,cv2.MORPH_ERODE,kernel)
        img= cv2.morphologyEx(img,cv2.MORPH_DILATE,kernel,iterations=2)
        img= cv2.threshold(img, 128, 255, cv2.THRESH_BINARY| cv2.THRESH_OTSU)[1]

        cv2.imshow('img',img)
        cv2.imshow('cam',cam)
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break
    cv2.destroyAllWindows()

    kp,des=detect.detectAndCompute(img,None)

    imgWkp=cv2.drawKeypoints(img,kp,None)

    cv2.imshow('img',img)
    cv2.imshow('kp',imgWkp)
    key=cv2.waitKey(0)
    if key!=ord('r'):
        desList.append(des)
    cv2.destroyAllWindows()

while True:
    ret,frame=cap.read()
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frame=cv2.bilateralFilter(frame,9,300,150)
    frame= cv2.GaussianBlur(frame,(5,5),0)
    frame= fgbg.apply(frame,learningRate=0)
    frame= cv2.morphologyEx(frame,cv2.MORPH_ERODE,kernel)
    frame= cv2.morphologyEx(frame,cv2.MORPH_DILATE,kernel,iterations=5)
    frame= cv2.threshold(frame, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    kpt,dest=detect.detectAndCompute(frame,None)
    showImg=cv2.drawKeypoints(frame,kpt,None)
    #matches=[]
    ratGood=0
    index=-1
    for i,d in enumerate(desList):
        try:
            matches=matcher.knnMatch(d,dest,k=2)
        except:
            cv2.imshow('img',showImg)
            continue

        if not matches is None:
            goodOnes=[]
            rat=0.0
            try:
                for m1,m2 in matches:
                    if m1.distance<0.75 * m2.distance:
                        goodOnes.append(m1)
                        rat+=1
            except:
                continue
            rat/=len(d)
            if rat>ratGood:
                ratGood=rat
                index=i
    if ratGood>thresh:
        print(ratGood)
        cv2.putText(showImg, str(index), textOrg,cv2.FONT_HERSHEY_SIMPLEX,1,[255,255,255])
    else:
        cv2.putText(showImg, 'no macthes', textOrg,cv2.FONT_HERSHEY_SIMPLEX,1,[255,255,255])
    cv2.imshow('img',showImg)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break
cap.release()
