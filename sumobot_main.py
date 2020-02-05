#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

# Write your program here
brick.sound.beep()

right_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
left_motor = Motor(Port.D, Direction.COUNTERCLOCKWISE)
lifter = Motor(Port.B)

left_color = ColorSensor(Port.S1)
right_color = ColorSensor(Port.S4)

my_distance = UltrasonicSensor(Port.S2)

on_table = True
while True:

    while on_table:
        right_motor.run(700)
        left_motor.run(700)
        if my_distance.distance() < 200:
            lifter.run_angle(500, 200)
            lifter.run_angle(500,-200)
            print(my_distance.distance())
        if left_color.color()== None or right_color.color() == None:
            on_table = False

    if not on_table:
        right_motor.stop(Stop.BRAKE)
        left_motor.stop(Stop.BRAKE)
        wait(50)
        while left_color.color() != None:
            left_motor.run(200)
            right_motor.run(-200)
        while right_color.color() != None:
            right_motor.run(200)
            left_motor.run(-200)

        right_motor.run(-400)
        left_motor.run(-400)
        wait(1000)
        print('backwards')
        on_table = True
        while my_distance.distance() > 400:
            left_motor.run(300)
            right_motor.run(-300)
            print('yay!')
