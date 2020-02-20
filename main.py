#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import serial
import time

# Write your program here
ev3 = EV3Brick()
ev3.speaker.beep()

# Returns an array with IMU data
def collectIMU(s):
    tmp = []
    while True:
        data=s.read(s.inWaiting()).decode("utf-8")
        if len(data) != 0:
            data = data.splitlines()
            data = data[0].split(',')
            if len(data) == 6:
                try:
                    for item in data:
                        tmp.append(float(item))
                    return tmp
                except:
                    continue



def averageCol(data, col):
    tmp = []
    for item in data:
        tmp.append(item[col])
    return sum(tmp) / len(tmp)

def playMusic(imumeans, threshold, note_time):
    global curr_time
    # First check positive rotation
    # Roll
    if time.time() - curr_time < 0.1:
        return
    curr_time = time.time()

    if ((abs(imumeans[3]) > threshold[0]) and (imumeans[3] > 0)):
        ev3.speaker.beep(261, note_time)
    # Pitch
    elif ((abs(imumeans[4]) > threshold[1]) and (imumeans[4] > 0)):
        ev3.speaker.beep(220, note_time)
    # Yaw
    elif ((abs(imumeans[5]) > threshold[2]) and (imumeans[5] > 0)):
        ev3.speaker.beep(196, note_time)
    # Then check negative rotation
    # Roll
    elif ((abs(imumeans[3]) > threshold[0]) and (imumeans[3] < 0)):
        ev3.speaker.beep(330, note_time)
    # Pitch
    elif ((abs(imumeans[4]) > threshold[1]) and (imumeans[4] < 0)):
        ev3.speaker.beep(147, note_time)
    # Yaw
    elif ((abs(imumeans[5]) > threshold[2]) and (imumeans[5] < 0)):
        ev3.speaker.beep(294, note_time)

imumeans = [0, 0, 0, 0, 0, 0]
threshold = [200, 200, 200]
imuinit = []
s=serial.Serial("/dev/ttyACM0",9600)
note_time = 300
curr_time = time.time()


while True:
    imuarray = collectIMU(s)
    print(imuarray)

    playMusic(imuarray, threshold, note_time)

    #print(imumeans)
