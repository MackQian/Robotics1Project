import time
from controller import Robot
from controller import Keyboard
from keys import *
from movement_commands import *

#commands with zero or one finger(s)
def command0(k):
    #close the fingers
    if k==KEY_F:
        grip()
    #reset the arm
    elif k==KEY_G:
        reset()
    #stop the wheels
    else:
        stop()
#commands with two finger
def command2(key):
    #collect the item
    if key==KEY_F:
        collect()
    #move the arm forward
    elif key==KEY_G:
        rotate_forward()
    #move the wheels forward
    else:
        move_forward()
#commands with three fingers
def command3(key):
    #release the item
    if key==KEY_F:
        release()
    #move the arm backward
    elif key==KEY_G:
        rotate_backward()
    #move the wheels backward
    else:
        move_backward()
#commands with four fingers
def command4(key):
    #reach far
    if key==KEY_F:
        reach_far()
    #turn the arm left
    elif key==KEY_G:
        rotate_left()
    #turn the wheels left
    else:
        turn_left()
#commands with five fingers
def command5(k):
    if k==KEY_F:
        print("reach_high")
        reach_high()
    #turn the arm right
    elif k==KEY_G:
        print("rotate_right")
        rotate_right()
    #turn the wheels right
    else:
        print("turn_right")
        turn_right()

