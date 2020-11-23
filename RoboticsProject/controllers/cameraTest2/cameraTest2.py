"""cameraTest2 controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
import cv2
import numpy as np
#install with pip install scikit-image
from skimage.measure import compare_ssim

import math
KEY_F=70
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


#accesss this var to get the gesture
#CURRENTLY 1 FINGER UP and 0 FINGERS ARE IDENTICAL
#FOR BEST RESULTS USE WITH CONTRAST BACKGROUND TO HAND
fingerCount=0

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
        #source: https://medium.com/analytics-vidhya/hand-detection-and-finger-counting-using-opencv-python-5b594704eb08
        if defects is not None:
            count=0
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                cv2.line(frame,start,end,[0,255,0],2)
                #compute triangle from the contour
                a = np.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = np.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = np.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                angle = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
                if angle <= np.pi/2:  # angle less than 90 degree, treat as finger gaps
                    count += 1
                    cv2.line(frame,start,far,[255,0,0],2)
                    cv2.line(frame,far,end,[255,0,0],2)
                    cv2.circle(frame, far, 4, [0, 0, 255], -1)
            if count > 0:
              count = count+1
            fingerCount=count
            cv2.putText(frame, str(fingerCount), textOrg,cv2.FONT_HERSHEY_SIMPLEX,1,[255,255,255])
    else:
        th = np.zeros(roi.shape, dtype='uint8')
    
    cv2.imshow('diff',diff)
    cv2.imshow('sanitized',th)
    cv2.imshow('Frame',frame)
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
