"""movementTest2 controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Keyboard
import numpy as np
from commands import *
KEY_W=87
KEY_A=65
KEY_S=83
KEY_D=68
KEY_R=82
KEY_H=72
KEY_C=67
KEY_Z=90
KEY_G=71
KEY_F=70
KEY_I=73
# create the Robot instance.
robot = Robot()

def display_helper_message():
    print("Control commands:\n");
    print(" Arrows:       Move the robot\n");
    print(" WASD: Control the robot arm\n");
    print(" Space: Reset\n");

def commands(i):
    switcher={
            KEY_W: rotate_forward,
            KEY_A: rotate_left,
            KEY_S: rotate_backward,
            KEY_D: rotate_right,
            Keyboard.UP: move_forward
    }
    func=switcher.get(i,lambda:"Invalid Command")
    return func()
# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

gps=robot.getGPS("gps")
gps.enable(timestep)
gripper_init(robot)
arm_init(robot)
base_init(robot)

keyboard=Keyboard()
keyboard.enable(timestep)

display_helper_message()
while robot.step(timestep)!=-1:
    key=keyboard.getKey()
    if(key!=-1):
        commands(key)
    
# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getMotor('motorname')
#  ds = robot.getDistanceSensor('dsname')
#  ds.enable(timestep)

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
