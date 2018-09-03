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

hum_mode = open("bin/current_hum_mode", "r").readline()
lamp_mode = open("bin/current_lamp_mode", "r").readline()

vent_mode_pattern = r"v\w\d"
hum_mode_pattern = r"h\w\d"
lamp_mode_pattern = r"l\w\d"

try:
    while True:
        fan_thread(open("bin/current_vent_mode", "r").readline())
        time.sleep(1)
    	#fan_thread("10/20")
except KeyboardInterrupt:
    print('interrupted!')
