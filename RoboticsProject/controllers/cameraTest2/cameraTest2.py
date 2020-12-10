"""cameraTest2 controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
import cv2
import numpy as np
from controller import Keyboard
from movement_commands import *
from gesture_commands import *

import math
KEY_F=70
def display_helper_message():
    print("Gesture commands:\n");
    print(" 0 Fingers + W: Reset\n");
    print(" 0 Fingers + S:     Stop\n\n");

    print(" 2 Finger + W:  Move Forward\n");
    print(" 2 Finger + S:  Move Backward\n");
    print(" 2 Finger + A:  Turn Left\n");
    print(" 2 Finger + D:  Turn Right\n\n");

    print(" 3 Finger + W:  Rotate Forward\n");
    print(" 3 Finger + S:  Rotate Backward\n");
    print(" 3 Finger + A:  Rotate Left\n");
    print(" 3 Finger + D:  Rotate Right\n\n");

    print(" 4 Fingers + W: Grip\n");
    print(" 4 Fingers + S: Release\n\n");
    print(" 4 Fingers + A: Slide Left\n");
    print(" 4 Fingers + D: Slide Right\n\n");

    print(" 5 Fingers + W: Reach Far\n");
    print(" 5 Fingers + S: Reach In-Front\n");
    print(" 5 Fingers + A: Reach High\n\n");
    print(" 5 Fingers + D: Collect\n");
# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

#init vision stuff
cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2(0,50)
kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
matcher=cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_BRUTEFORCE_HAMMING)
detect=cv2.AKAZE.create()

textOrg=(20,50)

#can change to support more or less, but 5 to support the finger gap code
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


#initialize the robot
gripper_init(robot)
arm_init(robot)
base_init(robot)
keyboard=Keyboard()
keyboard.enable(2*timestep)
#display commands
display_helper_message()
#accesss this var to get the gesture
#CURRENTLY 1 FINGER UP and 0 FINGERS ARE IDENTICAL
#FOR BEST RESULTS USE WITH CONTRASTED BACKGROUND TO HAND
fingerCount=0

prevCount=0
key=keyboard.getKey()
prevkey=0

# array to store last prevNum computed gestures, used in deciding what gesture to output
prev=[]
prevNum=5

#threshold of similarity, must pass this to register as a gesture
thresh=.2

while robot.step(timestep) != -1:
    #read and clean
    ret,frame=cap.read()
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frame=cv2.bilateralFilter(frame,9,300,150)
    frame= cv2.GaussianBlur(frame,(5,5),0)
    frame= fgbg.apply(frame,learningRate=0)
    frame= cv2.morphologyEx(frame,cv2.MORPH_ERODE,kernel)
    frame= cv2.morphologyEx(frame,cv2.MORPH_DILATE,kernel,iterations=5)
    frame= cv2.threshold(frame, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    #compute key points
    kpt,dest=detect.detectAndCompute(frame,None)
    showImg=cv2.drawKeypoints(frame,kpt,None)

    ratGood=0
    index=-1

    #loop to compare defined gestures to camera input
    for i,d in enumerate(desList):
        #find keypoint matches
        try:
            matches=matcher.knnMatch(d,dest,k=2)
        except:
            cv2.imshow('img',showImg)
            continue
        #find the actual good ones with Lowes ratio test
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
            #compute ratio of matches to number of gesture keypoints
            rat/=len(d)
            if rat>ratGood:
                ratGood=rat
                index=i
    #compare against threshold
    if ratGood>thresh and index !=-1:
        print(index)
        prevCount=fingerCount
        #slow update for less twitchiness
        fingerCount=index
        if len(prev)<prevNum:
            prev.append(fingerCount)
        else:
            temp=max(prev,key=prev.count)
            prev.pop(0)
            prev.append(fingerCount)
            fingerCount=temp
        cv2.putText(showImg, str(fingerCount), textOrg,cv2.FONT_HERSHEY_SIMPLEX,1,[255,255,255])
    #no matches
    else:
        cv2.putText(showImg, 'no matches', textOrg,cv2.FONT_HERSHEY_SIMPLEX,1,[255,255,255])
        fingerCount=-1
    cv2.imshow('img',showImg)

    # the match command module
    prevkey=key
    key=keyboard.getKey()
    if fingerCount==4 and (prevCount!=fingerCount or prevkey!=key):
        command5(key)
    elif fingerCount==3 and (prevCount!=fingerCount or prevkey!=key):
        command4(key)
    elif fingerCount==2 and (prevCount!=fingerCount or prevkey!=key):
        command3(key)
    elif fingerCount==1 and (prevCount!=fingerCount or prevkey!=key):
        command2(key)
    elif fingerCount==0 and (prevCount!=fingerCount or prevkey!=key):
        command0(key)
    elif fingerCount==-1:
        stop()

    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break
    #USE THIS TO RECALIBRATE THE BACKGROUND, kinda buggy, hold down R until camera freezes
    if (cv2.waitKey(1) & 0xFF == ord('r')):
        fgbg = cv2.createBackgroundSubtractorMOG2(0,50)
cap.release()
cv2.destroyAllWindows()
