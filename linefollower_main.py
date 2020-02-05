#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

from pybricks.ev3devio import Ev3devSensor 
import utime
import ev3dev2
from ev3dev2.port import LegoPort

class MySensor(Ev3devSensor):  #Define Class 
    _ev3dev_driver_name="ev3-analog-01"
    #do not forget to set port mode to EV3-Analog 
    def readvalue(self):
        self._mode('ANALOG')
        return self._value(0)


# Before running the code go to Device Browser and Sensors. Make sure you can see ev3-analog-01, otherwise you will get an error.

# Write your program here
def main():
    brick.sound.beep()
    sens1 = LegoPort(address ='ev3-ports:in4') # which port?? 1,2,3, or 4
    #sens2 = LegoPort(address ='ev3-ports:in4') # which port?? 1,2,3, or 4
   
    sens1.mode = 'ev3-analog'
    #sens2.mode = 'ev3-analog'
   
    utime.sleep(0.5)   

    sensor_left = MySensor(Port.S4) # same port as above
    sensor_right = MySensor(Port.S2) # same port as above

    left_motor = Motor(Port.A)
    right_motor = Motor(Port.D)
    speed = 200

    Kp = 3
    speed = 250
    Kd = 0.4
    diff = 0
    curr_gain = 0.8
    last = [0, 0]

    while True:
        difflast = diff
        left_color = sensor_left.readvalue()
        right_color = sensor_right.readvalue()
        if last is [0, 0]:
            last = [left_color, right_color]
        left_color, right_color = left_color*curr_gain + (last[0] * (1-curr_gain)), right_color*curr_gain + (last[1] * (1-curr_gain))
        last = [left_color, right_color]
        diff = left_color - right_color
        deriv = diff - difflast
        # print(diff)
        # print(deriv)
        print("Left: {}, Right: {}, Diff: {}".format(left_color, right_color, diff))
        controller = ((Kp * diff) + (Kd + deriv))/2
        left_motor.run(speed + controller)
        right_motor.run(speed - controller)

main()
