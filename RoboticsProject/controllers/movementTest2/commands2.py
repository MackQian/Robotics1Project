import time
from controller import Robot
from controller import Keyboard
from keys import *
from commands import *

#commands with zero fingers
def command0(key):
    #close the fingers
    if key==Keyboard.ALT:
        grip()
    #reset the arm
    elif key==Keyboard.SHIFT:
        reset()
    #stop the wheels
    else:
        stop(0
#commands with one finger
def command1(key):
    #collect the item
    if key==Keyboard.ALT:
        collect()
    #move the arm forward
    elif key==Keyboard.SHIFT:
        rotate_forward()
    #move the wheels forward
    else:
        move_forward()
#commands with two fingers
def command2(key):
    #release the item
    if key==Keyboard.ALT:
        release()
    #move the arm backward
    elif key==Keyboard.SHIFT:
        rotate_backward()
    #move the wheels backward
    else:
        move_backward()
#commands with three fingers
def command3(key):
    #turn the arm left
    if key==Keyboard.SHIFT:
        rotate_left()
    #turn the wheels left
    else:
        turn_left()
#commands with four fingers
def command4(key):
    #turn the arm right
    if key==Keyboard.SHIFT:
        rotate_right()
    #turn the wheels right
    else:
        turn_right()
#commands with five fingers
def command5(key):
    #reach far
    if key==Keyboard.SHIFT:
        reach_far()
    #reach high
    else:
        reach_high()
