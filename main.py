#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.iodevices import AnalogSensor, UARTDevice


# Write your program here
ev3 = EV3Brick()
ev3.speaker.beep()

def redLEGO():
    #motor.reset(0)
    motor.run_angle(300,90)
    motor.run_angle(-300,90)
    print('redlego')

def badLEGO():
    #motor.reset(0)
    motor.run_angle(-300,90)
    motor.run_angle(300,90)
    print('badlego')

def readSerial():
    try:
        #uart.write("HelloRpi".encode())
        # msg = uart.read(uart.waiting()) # not too many options on pybricks micropython
        msg = uart.read(1)
        msg = msg.decode('utf-8')
        print(msg)
        return msg

    except:
        pass

def writeSerial(message):
    try:
        uart.write(message.encode())
        print('message sent!')
    except:
        print('failed to send')


uart = UARTDevice(Port.S1, 9600, timeout=200)
motor = Motor(Port.D)
writeSerial('P')

while True:

    msg = readSerial()
    #print(msg)

    if msg == 'R':
        redLEGO()
    elif msg == 'N':
        badLEGO()
    else:
        continue
    ev3.speaker.beep()
    writeSerial('P')
