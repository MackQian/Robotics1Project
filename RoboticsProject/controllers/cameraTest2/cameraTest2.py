"""cameraTest2 controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
import cv2
import numpy as np
from controller import Keyboard
from movement_commands import *
from gesture_commands import *
#install with pip install scikit-image
from skimage.measure import compare_ssim

import math
KEY_F=70
def display_helper_message():
    print("Gesture commands:\n");
    print(" 0 Fingers + F: Grip\n");
    print(" 0 Fingers + G: Reset\n");
    print(" 0 Fingers:     Stop\n");
    
    print(" 2 Finger + F:  Collect\n");
    print(" 2 Finger + G:  Rotate Forward\n");
    print(" 2 Finger:      Move Forward\n");
    
    print(" 3 Fingers + F: Release\n");
    print(" 3 Fingers + G: Rotate Backward\n");
    print(" 3 Fingers:     Move Forward\n");
    
    print(" 4 Fingers + F: Reach Far\n");
    print(" 4 Fingers + G: Rotate_Left\n");
    print(" 4 Fingers:     Turn Left\n");
    
    print(" 5 Fingers + F: Reach High\n");
    print(" 5 Fingers + G: Rotate Right\n");
    print(" 5 Fingers:     Turn Right\n");
# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())
# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getMotor('motorname')
#  ds = robot.getDistanceSensor('dsname')
#  ds.enable(timestep)

#recalibrates the background
def noiseCalibrate(cap,rob,bbLC,bbRC):
    diffPercent=0
    for i in range(30):
        ret,frame=cap.read()
        roi=frame[bbLC[0]:bbRC[0], bbLC[1]:bbRC[1]]
        (score,diff)=compare_ssim(rob,roi,full=True,multichannel=True)
        diffPercent+=score
    diffPercent/=30
    return diffPercent-.03
#get camera device
cap = cv2.VideoCapture(0)

bbLC=(0,0)
bbRC=(300,300)
textOrg=(20,50)
kernel=np.ones((5,5),np.uint8)

dontcare,temp=cap.read()
rob=temp[bbLC[0]:bbRC[0], bbLC[1]:bbRC[1]]

#compute mean image difference so code doesnt pick up noise
diffPercent=noiseCalibrate(cap,rob,bbLC,bbRC)

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

while robot.step(timestep) != -1:

    ret,frame=cap.read()
    roi=frame[bbLC[0]:bbRC[0], bbLC[1]:bbRC[1]]
    (score,diff)=compare_ssim(rob,roi,full=True,multichannel=True)
    cv2.rectangle(frame,bbLC,bbRC,(0,255,0),0)
    #if the new frame is different enough from the background, run the following...
    if(score<diffPercent):
        #get the difference matrix into an image
        diff = (diff * 255).astype("uint8")
        #reduces noise
        diff = cv2.morphologyEx(diff,cv2.MORPH_OPEN,kernel)
        #conv to grayscale
        diff = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
        #more noise reduction/ fills in gaps on the hand
        diff = cv2.GaussianBlur(diff,(5,5),100)
        #convert into binary image, extracts hand shape basically
        th= cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV| cv2.THRESH_OTSU)[1]
        #compute contours of the hand
        cnt, hierarchy = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnt = max(cnt, key=lambda x: cv2.contourArea(x))
        cv2.drawContours(frame, [cnt], -1, (255,255,0), 2)
        #compute convex hull and find defects to find finger gaps
        hull = cv2.convexHull(cnt,returnPoints = False)
        defects = cv2.convexityDefects(cnt,hull)
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
                if angle <= np.pi/2:  # angle less than 90 degree, treat as finger gaps
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
        th = np.zeros(roi.shape, dtype='uint8')
    
    cv2.imshow('diff',diff)
    cv2.imshow('sanitized',th)
    cv2.imshow('Frame',frame)
    prevkey=key
    key=keyboard.getKey()
    if fingerCount==5 and (prevCount!=fingerCount or prevkey!=key):
        command5(key)
    elif fingerCount==4 and (prevCount!=fingerCount or prevkey!=key):
        command4(key)
    elif fingerCount==3 and (prevCount!=fingerCount or prevkey!=key):
        command3(key)
    elif fingerCount==2 and (prevCount!=fingerCount or prevkey!=key):
        command2(key)
    elif fingerCount==0 and (prevCount!=fingerCount or prevkey!=key):
        command0(key)
    
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break
    #USE THIS TO RECALIBRATE THE BACKGROUND, kinda buggy, hold down R until camera freezes
    if (cv2.waitKey(1) & 0xFF == ord('r')):
        dontcare,temp=cap.read()
        rob=temp[bbLC[0]:bbRC[0], bbLC[1]:bbRC[1]]
        diffPercent=noiseCalibrate(cap,rob,bbLC,bbRC)
        bkgrem=cv2.bgsegm.createBackgroundSubtractorGSOC(replaceRate=0,propagationRate=0)
cap.release()
cv2.destroyAllWindows()

# Enter here exit cleanup code.
