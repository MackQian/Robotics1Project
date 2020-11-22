"""cameraTest2 controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
import cv2
import numpy as np
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
def noiseCalibrate(cap,rob,bbLC,bbRC):
    diffPercent=0
    for i in range(30):
        ret,frame=cap.read()
        roi=frame[bbLC[0]:bbRC[0], bbLC[1]:bbRC[1]]
        roi2=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
        (score,diff)=compare_ssim(rob,roi2,full=True)
        diffPercent+=score
    diffPercent/=30
    return diffPercent-.03
cap = cv2.VideoCapture(0)
bbLC=(0,0)
bbRC=(300,300)

kernel=np.ones((5,5),np.uint8)
dontcare,temp=cap.read()
rob=temp[bbLC[0]:bbRC[0], bbLC[1]:bbRC[1]]
rob=cv2.cvtColor(rob,cv2.COLOR_BGR2GRAY)

diffPercent=noiseCalibrate(cap,rob,bbLC,bbRC)

while True:
    ret,frame=cap.read()
    roi=frame[bbLC[0]:bbRC[0], bbLC[1]:bbRC[1]]
    roi2=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
    (score,diff)=compare_ssim(rob,roi2,full=True)
    cv2.rectangle(frame,bbLC,bbRC,(0,255,0),0)
    print(score," ",diffPercent)
    if score<diffPercent:
        diff = (diff * 255).astype("uint8")
        diff = cv2.morphologyEx(diff,cv2.MORPH_OPEN,kernel)
        th= cv2.threshold(diff, 128, 255, cv2.THRESH_TOZERO_INV| cv2.THRESH_OTSU)[1]
        contours = cv2.findContours(th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        mask = np.zeros(roi.shape, dtype='uint8')
        for c in contours:
            area = cv2.contourArea(c)
            if area > 40:
                cv2.drawContours(mask, [c], 0, (0,255,0), -1)
        contours1, hierarchy = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours1 = max(contours1, key=lambda x: cv2.contourArea(x))
        cv2.drawContours(frame, [contours1], -1, (255,255,0), 2)
    else:
        mask = np.zeros(roi.shape, dtype='uint8')
        th = np.zeros(roi.shape, dtype='uint8')
    cv2.imshow('diff',diff)
    cv2.imshow('thresh',th)
    cv2.imshow('frame2',frame)
    cv2.imshow('sanitized',mask)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break
    if (cv2.waitKey(1) & 0xFF == ord('r')):
        dontcare,temp=cap.read()
        rob=temp[bbLC[0]:bbRC[0], bbLC[1]:bbRC[1]]
        rob=cv2.cvtColor(rob,cv2.COLOR_BGR2GRAY)
        diffPercent=noiseCalibrate(cap,rob,bbLC,bbRC)
cap.release()
cv2.destroyAllWindows()

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass

# Enter here exit cleanup code.
