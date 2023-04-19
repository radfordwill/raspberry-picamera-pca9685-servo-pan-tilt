#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on Wed Apr 19 09:44:23 2023
@author: Will Radford
This file tests a 2 axis gimbal with a raspberry pi camera v1.3
and two sg90 servos controlled and powered by a pca9685 board
"""

import pynput.keyboard
from pynput.keyboard import Key, Listener
import os,sys,time
from board import SDA,SCL
import busio
from picamera import PiCamera
from adafruit_servokit import ServoKit

global camera, pan_servo_pos, tilt_servo_pos

# min and max servo pulse lengths
pan_servo = 5
pan_min = 0
pan_mid = 90
pan_max = 180
pan_servo_pos = pan_mid
tilt_servo = 7
tilt_min = 0
tilt_mid = 90
tilt_max = 140
tilt_servo_pos = tilt_mid

# ServoKit    
kit = ServoKit(channels=16)

# picamera with exception
def setup():
    try:
        # Set up camera
        camera = PiCamera()
        camera.start_preview(fullscreen=False, window = (100,20,320,240))
        # center servos
        kit.servo[pan_servo].angle = pan_servo_pos 
        kit.servo[tilt_servo].angle = tilt_servo_pos 
    except:
        camera.stop_preview()
        print("picamera exception")      
    else:
        print("picamera started")
        
# Setting start up servo positions
def show(key):
    global pan_servo_pos, tilt_servo_pos

    if key == key.right:
        print('right key')
        pan_servo_pos = max(pan_servo_pos-2, pan_min+1)
        kit.servo[pan_servo].angle = pan_servo_pos 
        time.sleep(0.005)
    elif key == key.left:
        print('left key')
        pan_servo_pos = min(pan_servo_pos+2, pan_max-1)
        kit.servo[pan_servo].angle = pan_servo_pos 
        time.sleep(0.005)
    elif key == key.down:
        print('down key')
        tilt_servo_pos = max(tilt_servo_pos-2, tilt_min+1)
        kit.servo[tilt_servo].angle = tilt_servo_pos 
        time.sleep(0.005)
    elif key == key.up:
        print('up key')
        tilt_servo_pos = min(tilt_servo_pos+2, tilt_max-1)
        kit.servo[tilt_servo].angle = tilt_servo_pos 
        time.sleep(0.005)

# main program
try:
    setup()

    with Listener(on_press = show) as listener:
        listener.join()
    
except (Exception, KeyboardInterrupt):
    sys.exit('stopped')