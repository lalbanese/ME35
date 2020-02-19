#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# Write your program here
ev3 = EV3Brick()
ev3.speaker.beep()

# '''
# This reads the USB serial line on the EV3 as fast as possible
# and assumes that data is coming from the Arduino much faster
# than we can read it - so it grabs all the data, splits it up into an array,
# and then takes the second to last element of that array to get an
# array of accelerations and angular accelerations.
# The 6 elements are:
#      x acceleration
#      y acceleration
#      z acceleration
#      x gyro
#      y gyro
#      z gyro
     
# Note that I take the second to last line because the last line might be incomplete
# (who knows where in the serial transmission the line is when I do the read).
# '''

count = 0
imumeans = [0, 0, 0, 0, 0, 0]

import serial
s=serial.Serial("/dev/ttyACM0",9600)

while True:
     data=s.read(s.inWaiting()).decode("utf-8")
     #print('size = %d, buffer = %d' % (len(data),s.inWaiting()))
     if len(data) != 0:
        data = data.splitlines()
        imu = data[0].split(',')
        #print(data)
        #print(imu)

        if imu == ['']:
            continue

        count = count+1
        try:
            for i in range(len(imu)):
                #print(type(imu[i]))
                #print(imu[i])
                imu[i] = float(imu[i])

            #print(type(imu[0]))
            for means in range(len(imumeans)):
                imumeans[means] = (imumeans[means]+imu[means])/(count)

        except:
            print("ERROR")
            print(data)
            print(imu)
            print(type(imu[0]))
