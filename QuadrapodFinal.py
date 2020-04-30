#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import ubinascii, ujson, urequests, utime
#import passwords

# Write your program here
ev3 = EV3Brick()
ev3.speaker.beep()

import ubinascii, ujson, urequests, utime
     
Key = 'bvd8X9LweQY9o2eP1NYL-p8mLL9wMAk6YYOnYSiIo0'
     
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

def PD_Controller(err,Kp,Kd,speed):
     errlast = err
     left_ref = left_sens.reflection()
     right_ref = right_sens.reflection()
     err = left_ref - right_ref
     deriv = err - errlast
     pd = ((Kp * err) + (Kd + deriv))/2
     left_motor.run(speed-pd)
     right_motor.run(speed+pd)
     print(err)

def End_Sequence(nxt,trigger):
     left_motor.stop()
     right_motor.stop()
     while nxt == False:
          Put_SL('Start17','BOOLEAN','true')
          nxt = Get_SL('Start17')
          nxt = True if nxt == 'true' else False
     while trigger == True:
          Put_SL('Start16','BOOLEAN','false')
          trigger = Get_SL('Start16')
          trigger = True if trigger == 'true' else False
     print('done')

left_motor = Motor(Port.D)
right_motor = Motor(Port.A)
left_sens = ColorSensor(Port.S2)
right_sens = ColorSensor(Port.S3)
dist_sens = UltrasonicSensor(Port.S4)
Kp = 45
Kd = 0.5
err = 0
speed = 400
nxt = Get_SL('Start17')
nxt = True if nxt == 'true' else False

while True:
     trigger = Get_SL('Start16')
     trigger = True if trigger == 'true' else False
     
     if trigger == True:
          PD_Controller(err,Kp,Kd,speed)
          dist = dist_sens.distance()
          print(dist)
          if dist < 100:
               #print('done')
               #left_motor.stop()
               #right_motor.stop()
               End_Sequence(nxt,trigger)
