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

uart = UARTDevice(Port.S2, 9600, timeout=2000)
driveMotor = Motor(Port.D)
lightSens = ColorSensor(Port.S1)
xMotor = Motor(Port.C)
spdx = 1000
spdy = 300
angx = -5000
angy = 330
threshold = 5

def DriveX(speedx,anglex):
    xMotor.reset_angle(0)
    while xMotor.angle() > anglex:
        xMotor.run(-speedx)
        refl = lightSens.reflection()
        print("AngleX: {}, Angle: {}, Light: {}".format(anglex, xMotor.angle(), refl))
        if refl >= threshold
            uart.write('T')
    print('turning around')
    xMotor.stop(stop_type = Stop.BRAKE)
    wait(10)
    xMotor.reset_angle(0)
    while xMotor.angle() < -anglex:
        xMotor.run(speedx)
        print("AngleX: {}, Angle: {}".format(anglex, xMotor.angle()))


def DriveY(speedy,angley):
    driveMotor.run_angle(speedy,angley)

while True:
    if uart.waiting() >= 1:
        msg = uart.read(1)
        if msg == 'x':
            DriveX(spdvaluex, angx)

        elif msg == 'y':
            DriveY(spdvaluey, angy)