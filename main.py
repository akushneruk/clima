#!/usr/bin/env python3
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

try:
    while True:
        fan_thread("10/20")
	readSerial()
except KeyboardInterrupt:
    print('interrupted!')
