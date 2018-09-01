#!/usr/bin/env python2
import time
import serial
import sys
import RPi.GPIO as GPIO
from mode import *
from send import *


#---INIT--
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
channel = [6, 13, 19, 26]
ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

#--Setup
intiGpio(channel)
x=ser.readline()
print(str(x))

try:
    while True:
        #fan_thread("10/20")
        x=ser.readline()
	print(x)
        time.sleep(1)
except KeyboardInterrupt:
    print('interrupted!')
