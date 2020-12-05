import time
from controller import Robot
from controller import Keyboard
from keys import *
from movement_commands import *

#commands with zero or one finger(s)
def command0(key):
    if key==KEY_W:
        reset()
    #stop moving the wheels
    elif key==KEY_S:
        stop()
#commands with two fingers
def command2(key):
    #move base forward
    if key==KEY_W:
        move_forward()
    #move base backward
    elif key==KEY_S:
        move_backward()
    #turn base left
    elif key==KEY_A:
        turn_left()
    #turn the base right
    elif key==KEY_D:
        turn_right()
#commands with three fingers
def command3(key):
    #rotate the arm forward
    if key==KEY_W:
        rotate_forward()
    #rotate the arm backward
    elif key==KEY_S:
        rotate_backward()
    #rotate the arm left
    elif key==KEY_A:
        rotate_left()
    #rotate the arm right
    elif key==KEY_D:
        rotate_right()
#commands with four fingers
def command4(key):
    #reach far
    if key==KEY_W:
        grip()
    #reach high
    elif key==KEY_S:
        release()
    #slide left
    elif key==KEY_A:
        slide_left()
    #slide right
    elif key==KEY_D:
        slide_right()
#commands with five fingers
def command5(key):
    #grip an object
    if key==KEY_W:
        reach_far()
    #release grip
    elif key==KEY_S:
        reach_in_front()
    #put object over platform
    elif key==KEY_A:
        reach_high()
    elif key==KEY_D:
        collect()

