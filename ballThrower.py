#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import math

# Write your program here
ev3 = EV3Brick()
ev3.speaker.beep()

import ubinascii, ujson, urequests, utime
     
Key = 'KjpPmCDIP1kKpJ9BiDddyDbG-a7pRlJLi12IBShHtJ'

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

 #physics model:         
def newtDistanceRead(g,r,theta,distanceSens,motor1,motor2):
    x = distanceSens.distance()
    print(x)
    num = math.sqrt(g) * x
    den = math.sqrt(2) * math.sqrt(abs((-h*theta*theta) - (theta*theta*x)))
    w = c*num/den
    print(w)
    
    motor1.run_angle(w, -360, wait = False)
    motor2.run_angle(w, -360)
    return x, w

#training data:
def dataCollection(w,motor1,motor2):
    while w < 800:
        w = w+10
        print(w)
        wArray.append(w)
        motor1.run_angle(w, -360, wait = False)
        motor2.run_angle(w, -360)
        x = input('distance=')
        x = float(x)
        xArray.append(x)
    return wArray, xArray

#linear regression:
def mean(values):
    return sum(values) / float(len(values))

def variance(values, mean):
    return (sum([(x-mean)**2 for x in values]))

def covariance(xArray, mean_x, wArray, mean_w):
    covar = 0.0
    for k in range(len(xArray)):
        covar += (xArray[k] - mean_x) * (wArray[k] - mean_w)
    return covar

def coefficients(xArray, wArray):
    x_mean, w_mean = mean(xArray), mean(wArray)
    b1 = covariance(xArray, x_mean, wArray, w_mean) / variance(xArray, x_mean)
    b0 = w_mean - b1 * x_mean
    return[b0, b1]


def stats(xArray, wArray):
    mean_x, mean_w = mean(xArray), mean(wArray)
    var_x, var_w = variance(xArray,mean_x), variance(wArray,mean_w)
    covar = covariance(xArray,mean_x,wArray,mean_w)
    print('x stats: mean=%.3f variance = %.3f' % (mean_x, var_x))
    print('w stats: mean=%.3f variance = %.3f' % (mean_w, var_w))
    print('Covariance: %.3f' %(covar))

#using linear regression:
def distRead(distanceSens, b0, b1):
    x = distanceSens.distance()
    print(x)
    w = b0 + (b1 * (x+40)) 
    motor1.run_angle(w, -360, wait = False)
    motor2.run_angle(w, -360)
    return x, w

#main code:
distanceSens = UltrasonicSensor(Port.S1)
motor1 = Motor(Port.D)
motor2 = Motor(Port.A)

g = 9.81*1000
r = 66
theta = (360 * math.sqrt(2)) / (4 * 3.41)
h = 90
c = 40

#w = 100
#wArray = []
#xArray = []
#[wArray, xArray] = dataCollection(w,motor1,motor2)
#print(wArray)
#print(xArray)

#stats(xArray, wArray)
#b0, b1 = coefficients(xArray, wArray)
#print('Coefficients: B0=%.3f, B1 = %.3f' % (b0, b1))

b0 = 152.654
b1 = 2.218
x = 0
w = 0
while True:

    lin_str = Get_SL('runAlgorithm')
    phys_str = Get_SL('runPhysics')
    
    lin = True if lin_str =='true' else False
    phys = True if phys_str == 'true' else False

    print(phys)
    print(lin)

    if lin == True:
        [x,w] = distRead(distanceSens,b0,b1)

    if phys == True:
        [x,w] = newtDistanceRead(g,r,theta,distanceSens,motor1,motor2)
    x = str(x)
    w = str(w)
    Put_SL('newDistance', 'STRING', x)
    Put_SL('newSpeed', 'STRING', w)
