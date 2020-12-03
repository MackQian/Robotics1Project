"""movementTest2 controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Keyboard
from controller import Camera
from controller import TouchSensor
import numpy as np
import time
from movement_commands import *
#from commands2 import *
from keys import *

# create the Robot instance.
robot = Robot()

timestep = int(robot.getBasicTimeStep())
cam=robot.getCamera("camera")
cam.enable(timestep)


def display_helper_message():
    print("Control commands:\n");
    print(" Arrows:       Move the robot\n");
    print("Shift+left/right Slide the robot\n");
    print(" WASD: Control the robot arm\n");
    print(" F: Reach Far\n");
    print(" H: Reach High\n");
    print(" I: Reach In-Front\n");
    print(" C: Collect\n");
    print(" G: Grip\n");
    print(" R: Release\n");
    print(" Space: Reset\n");

def commands(i):
    switcher={
            KEY_W: rotate_forward,
            KEY_A: rotate_left,
            KEY_S: rotate_backward,
            KEY_D: rotate_right,
            KEY_H: reach_high,
            KEY_F: reach_far,
            KEY_I: reach_in_front,
            KEY_G: grip,
            KEY_C: collect,
            KEY_R: release,
            KEY_E: experiment,
            KEY_X: reset,
            SHIFT_RIGHT: slide_right,
            SHIFT_LEFT: slide_left,
            Keyboard.UP: move_forward,
            Keyboard.DOWN: move_backward,
            Keyboard.RIGHT: turn_right,
            Keyboard.LEFT: turn_left,
            KEY_SPACE: stop
            
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
keyboard.enable(2*timestep)

display_helper_message()
old_position = gps.getValues()
counts = 0
while robot.step(timestep)!=-1:
    new_position = gps.getValues()
    if (counts == 10):
        commands(KEY_SPACE)
        counts = 0
    if (abs(old_position[0] - new_position[0]) < 0.001 and abs(old_position[1] - new_position[1]) < 0.001 and abs(old_position[2] - new_position[2]) < 0.001):
        counts += 1
    else:
        counts = 0
    old_position = new_position
    key=keyboard.getKey()
    if(key!=-1):
        x=cam.getImage()
        #print(x)
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
