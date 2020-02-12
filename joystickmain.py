#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch, DataLog
from pybricks.robotics import DriveBase

import math
from pybricks.iodevices import AnalogSensor, UARTDevice

# Write your program here
brick.sound.beep()

joystick = Motor(Port.A)
indicator = Motor(Port.D)
xBut = TouchSensor(Port.S1)
yBut = TouchSensor(Port.S2)

sense = AnalogSensor(Port.S3, False)
uart = UARTDevice(Port.S3, 9600, timeout = 2000)

def VibrateMotor():
    joystick.run_angle(1400, 180)

def CompletionVibrate():
    indicator.run_time(1400, 700)

uart.clear()

while True: 
    while not (xBut.pressed() | yBut.pressed()):
        wait(100)
        if uart.waiting() > 0:
            msg = uart.read(1)
            uart.clear() #should clear automatically, but needed some help
            msg = str(msg)
            if msg[2] == 'T':
                VibrateMotor()
                print('|', end = '')
            elif msg[2] == 'F':
                print('.', end = '')
            elif msg[2] == 'C':
                CompletionVibrate()

    while (xBut.pressed() | yBut.pressed()):
        
        if xBut.pressed():
            uart.write('x') #send uart 'x'
            #print('wrote x')
        elif yBut.pressed():
            uart.write('y') #send uart 'y'
            #print('wrote y')
            print()
        if uart.waiting() > 0:
             VibrateMotor()
             uart.read(uart.waiting())
        
        wait(500)