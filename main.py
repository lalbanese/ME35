#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
from pybricks.iodevices import UARTDevice


# Write your program here
brick.sound.beep()

uart = UARTDevice(Port.S4, 9600, timeout=2000)
driveMotor = Motor(Port.D)
lightSens = ColorSensor(Port.S1)
xMotor = Motor(Port.C)
spdx = 1400
spdy = 300
angx = -16150
angy = -300
offset = 20

def Calibrate():
    startVal = lightSens.reflection()
    thres = startVal - offset
    return thres
    

def DriveX(speedx,anglex,thres):
    xMotor.reset_angle(0)
    while xMotor.angle() > anglex:
        xMotor.run(-speedx)
        #print(lightSens.reflection())
        #trigger motor if dark
        currentVal = lightSens.reflection()
        if currentVal < thres:
            print('uart is writing')
            uart.write('T')

    print('turning around')
    xMotor.stop(stop_type = Stop.BRAKE)
    wait(10)
    xMotor.reset_angle(0)

    while xMotor.angle() < -anglex:
        xMotor.run(speedx)
    xMotor.stop(stop_type = Stop.BRAKE)
    uart.write('C')
    print('finished scanning')
    


def DriveY(speedy,angley):
    driveMotor.run_angle(speedy,angley)
    uart.write('C')
    print('finished scanning')


#make it all happen!
uart.clear()
thres = Calibrate()
print('thres = ')
print(thres)

while True:
    if uart.waiting() >= 1:
        msg = uart.read(1)
        msg = str(msg)
        print(msg)
        if msg[2] == 'x':
            print(angx)
            DriveX(spdx, angx, thres)
        elif msg[2] == 'y':
            DriveY(spdy, angy)
        else:
            uart.clear()