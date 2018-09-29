#!/usr/bin/env python3
import os
import time
import datetime
import struct
import re
import serial
import RPi.GPIO as GPIO
from all import *

# Init
lamp_relay = 5
delay = 300

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(lamp_relay, GPIO.OUT, initial=1)

lamp_create = open("manual_lamp_mode", "w+")
lamp_create.seek(0)
lamp_create.truncate()
lamp_create.write("off")g
lamp_create.close()

try:
    while True:
        with open("manual_lamp_mode", 'r+') as file:
            for line in file:
                lamp = line
            file.seek(0)
        if lamp == "on":
            time.sleep(delay)
            GPIO.output(lamp_relay, 1)

            lamp_stop = open("manual_lamp_mode", "w+")
            lamp_stop.seek(0)
            lamp_stop.truncate()
            lamp_stop.write("off")
            lamp_stop.close()

            lamp_mode = open("current_lamp_mode", "w+")
            lamp_mode.seek(0)
            lamp_mode.truncate()
            lamp_mode.write("lt2")
            lamp_mode.close()

            nx_setValue(ser, 5,1,0)
            nx_setValue(ser, 5,2,0)
            nx_setValue(ser, 5,3,1)

except KeyboardInterrupt:
    pass