#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

# Write your program here


import ubinascii, ujson, urequests, utime
     
Key = 'KjpPmCDIP1kKpJ9BiDddyDbG-a7pRlJLi12IBShHtJ'
     
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
          

motor_back= Motor(Port.D)     
motor_direct = Motor(Port.B)
motor_arm = Motor(Port.A)

motor_direct.reset_angle(0)
motor_direct.reset_angle(0)

while True:
     #print(Get_SL('motor_move_please'))
     speed_str = Get_SL('motor_move_please')
     direction_str = Get_SL('direction')
     arm_str = Get_SL('arm_position')
     speed = float(speed_str)
     dir = float(direction_str)
     # print("Direction is: {}, type is {}".format(direction_str, type(direction_str)))
     arm_pos = True if arm_str == 'true' else False

     motor_back.run(speed)
     motor_direct.run_target(800, dir)
     #motor_direct.run_angle(800,dir)
     print(dir)
     print(arm_pos)
     if arm_pos == True:
          #motor_arm.run_angle(1000, -700,Stop.HOLD)
          motor_arm.run_target(800, -1100)
     elif arm_pos == False:
          #motor_arm.run_target(1000,700)
          motor_arm.run_target(800, 0)