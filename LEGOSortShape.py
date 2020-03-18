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

global speed
speed = 200

motorCups = Motor(Port.B)
motorBase = Motor(Port.C)
motorTilt = Motor(Port.D)
button = TouchSensor(Port.S1)

import ubinascii, ujson, urequests, utime
     
Key = 'gNoEmLvibS_TIXUPVOALnVjf9YhC8NijTM7AGlodDe'

#system link setup:     
def SL_setup():
     urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
     headers = {"Accept":"application/json","x-ni-api-key":Key}
     return urlBase, headers
     
def Put_SL(Tag, Type, Value):
     urlBase, headers = SL_setup()
     urlValue = urlBase + Tag + "/values/current"
     propValue = {"value":{"type":Type,"value":Value}}
     try:
          reply = urequests.put(urlValue,headers=headers,json=propValue).text
     except Exception as e:
          print(e)         
          reply = 'failed'
     return reply

def Get_SL(Tag):
     urlBase, headers = SL_setup()
     urlValue = urlBase + Tag + "/values/current"
     try:
          value = urequests.get(urlValue,headers=headers).text
          data = ujson.loads(value)
          #print(data)
          result = data.get("value").get("value")
     except Exception as e:
          print(e)
          result = 'failed'
     return result
     
def Create_SL(Tag, Type):
     urlBase, headers = SL_setup()
     urlTag = urlBase + Tag
     propName={"type":Type,"path":Tag}
     try:
          urequests.put(urlTag,headers=headers,json=propName).text
     except Exception as e:
          print(e)

def SortPiece(theta):
    global speed
    motorBase.run_target(speed,90)
    motorCups.run_target(speed/2,theta)
    motorTilt.run_target(speed,-45)
    wait(1000)
    motorTilt.run_target(speed, 0)
    wait(500)

def Return():
    global speed
    motorBase.run_target(speed,0)

def CheckPiece():
    global speed
    motorBase.run_target(speed,180)

theta = 0
motorCups.reset_angle(0)
motorBase.reset_angle(180)
Return()
motorTilt.reset_angle(0)

while True:
    while button.pressed() == False:
        pass
    CheckPiece()
    wait(2000)
    while True:
        shape = Get_SL('Piece_Shape')

        if shape == 'Gear':
            theta = 0
            SortPiece(theta)
            break

        elif shape == 'L':
            theta = 60
            SortPiece(theta)
            break

        elif shape == 'Three':
            theta = 120
            SortPiece(theta)
            break

        elif shape == 'Long':
            theta = 180
            SortPiece(theta)
            break

        elif shape == 'H':
            theta = 240
            SortPiece(theta)
            break

        elif shape == 'Angle135':
            theta = 300
            SortPiece(theta)
            break
    
    Return()
