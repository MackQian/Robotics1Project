import time
from controller import Robot

#initialize the arm
def arm_init(robot):
    global joint1
    global joint2
    global joint3
    global joint4
    global joint5
    joint1=robot.getMotor("arm1")
    joint2=robot.getMotor("arm2")
    joint3=robot.getMotor("arm3")
    joint4=robot.getMotor("arm4")
    joint5=robot.getMotor("arm5")
    joint1.setPosition(0)
    joint2.setPosition(0)
    joint3.setPosition(0)
    joint4.setPosition(0)
    joint5.setPosition(0)
#initialize the base
def base_init(robot):
    global wheel1
    global wheel2
    global wheel3
    global wheel4
    wheel1=robot.getMotor("wheel1")
    wheel2=robot.getMotor("wheel2")
    wheel3=robot.getMotor("wheel3")
    wheel4=robot.getMotor("wheel4")
#initialize the gripper
def gripper_init(robot):
    global finger1
    global finger2
    finger1=robot.getMotor("finger1")
    finger2=robot.getMotor("finger2")
#reach as far forward as possible
def reach_far():
    finger1.setPosition(0.025)
    finger2.setPosition(0.025)
    joint2.setPosition(-1.13)
    joint3.setPosition(-0.4)
    joint4.setPosition(-0.4)
    joint5.setPosition(0)
#reach as high as possible)
def reach_high():
    finger1.setPosition(0.025)
    finger2.setPosition(0.025)
    joint2.setPosition(0)
    joint3.setPosition(0)
    joint4.setPosition(-1.37)
    joint5.setPosition(0)
#for an object directly head
def reach_in_front():
    finger1.setPosition(0.025)
    finger2.setPosition(0.025)
    joint2.setPosition(-0.5)
    joint3.setPosition(-1)
    joint4.setPosition(-1.57)
    joint5.setPosition(0)
#rotate the arm left
def rotate_left():
    x=joint1.getTargetPosition()
    if x<2.8496:
        joint1.setPosition(x+0.1)
    else:
        joint1.setPosition(2.9496)
#rotate the arm right
def rotate_right():
    x=joint1.getTargetPosition()
    if x>-2.8496:
        joint1.setPosition(x-0.1)
    else:
        joint1.setPosition(-2.9496)
#rotate the arm backward
def rotate_backward():
    x=joint2.getTargetPosition()
    y=joint3.getTargetPosition()
    z=joint4.getTargetPosition()
    if x<1.5208:
        joint2.setPosition(x+0.05)
    else:
        joint2.setPosition(1.5708)
    if y<2.55:
        joint3.setPosition(x+0.0812)
    else:
        joint3.setPosition(2.55)
    if z<1.78:
        joint4.setPosition(x+0.0567)
    else:
        joint4.setPosition(1.78)
#rotate the arm forward
def rotate_forward():
    x=joint2.getTargetPosition()
    y=joint3.getTargetPosition()
    z=joint4.getTargetPosition()
    if x>-1.08446:
        joint2.setPosition(x-0.05)
    else:
        joint2.setPosition(-1.13446)
    if y>-2.5588:
        joint3.setPosition(x-0.0812)
    else:
        joint3.setPosition(-2.64)
    if z>-1.78:
        joint4.setPosition(x-0.0567)
    else:
        joint4.setPosition(-1.78)
#move the wheels forward
def move_forward():
    wheel1.setPosition(float('inf'))
    wheel1.setVelocity(4.0)
    wheel2.setPosition(float('inf'))
    wheel2.setVelocity(4.0)
    wheel3.setPosition(float('inf'))
    wheel3.setVelocity(4.0)
    wheel4.setPosition(float('inf'))
    wheel4.setVelocity(4.0)
#move the wheels backwards
def move_backward():
    wheel1.setPosition(float('inf'))
    wheel1.setVelocity(-4.0)
    wheel2.setPosition(float('inf'))
    wheel2.setVelocity(-4.0)
    wheel3.setPosition(float('inf'))
    wheel3.setVelocity(-4.0)
    wheel4.setPosition(float('inf'))
    wheel4.setVelocity(-4.0)
#rotate the base to the right
def turn_right():
    wheel1.setPosition(float('inf'))
    wheel1.setVelocity(-4.0)
    wheel2.setPosition(float('inf'))
    wheel2.setVelocity(4.0)
    wheel3.setPosition(float('inf'))
    wheel3.setVelocity(-4.0)
    wheel4.setPosition(float('inf'))
    wheel4.setVelocity(4.0)
#turn the base to the left
def turn_left():
    wheel1.setPosition(float('inf'))
    wheel1.setVelocity(4.0)
    wheel2.setPosition(float('inf'))
    wheel2.setVelocity(-4.0)
    wheel3.setPosition(float('inf'))
    wheel3.setVelocity(4.0)
    wheel4.setPosition(float('inf'))
    wheel4.setVelocity(-4.0)
#slide the base to the right without turning
def slide_right():
    wheel1.setPosition(float('inf'))
    wheel1.setVelocity(-4.0)
    wheel2.setPosition(float('inf'))
    wheel2.setVelocity(4.0)
    wheel3.setPosition(float('inf'))
    wheel3.setVelocity(4.0)
    wheel4.setPosition(float('inf'))
    wheel4.setVelocity(-4.0)
#slide the base to the left without turning
def slide_left():
    wheel1.setPosition(float('inf'))
    wheel1.setVelocity(4.0)
    wheel2.setPosition(float('inf'))
    wheel2.setVelocity(-4.0)
    wheel3.setPosition(float('inf'))
    wheel3.setVelocity(-4.0)
    wheel4.setPosition(float('inf'))
    wheel4.setVelocity(4.0)
#reset wheels and arm
def reset():
    finger1.setPosition(0)
    finger2.setPosition(0)
    joint1.setPosition(0)
    joint2.setPosition(0)
    joint3.setPosition(0)
    joint4.setPosition(0)
    joint5.setPosition(0)
    wheel1.setPosition(float('inf'))
    wheel1.setVelocity(0)
    wheel2.setPosition(float('inf'))
    wheel2.setVelocity(0)
    wheel3.setPosition(float('inf'))
    wheel3.setVelocity(0)
    wheel4.setPosition(float('inf'))
    wheel4.setVelocity(0)
def stop():
    wheel1.setPosition(float('inf'))
    wheel1.setVelocity(0)
    wheel2.setPosition(float('inf'))
    wheel2.setVelocity(0)
    wheel3.setPosition(float('inf'))
    wheel3.setVelocity(0)
    wheel4.setPosition(float('inf'))
    wheel4.setVelocity(0)
def grip():
    finger1.setPosition(0)
    finger2.setPosition(0)
def release():
    finger1.setPosition(0.025)
    finger2.setPosition(0.025)
def collect():
    joint1.setPosition(0)
    joint2.setPosition(0.5)
    joint3.setPosition(0.5)
    joint4.setPosition(1.6)
    joint5.setPosition(1.57)
def experiment():
    joint1.setPosition(0)
    joint2.setPosition(1.5708)
    joint3.setPosition(0)
    joint4.setPosition(0)
    joint5.setPosition(0)
