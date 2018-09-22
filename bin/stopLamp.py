#!/usr/bin/env python3
import os
import time
import datetime
import struct
import re
import serial
import RPi.GPIO as GPIO
from all import *

ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
ser.reset_output_buffer()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

lamp_relay = 26
delay = 1

try:
    while True:
        with open("current_lamp_mode", 'r+') as file:
            for line in file:
                lamp = line
            file.seek(0)
        stopLamp(lamp_relay, lamp)
        time.sleep(delay)
except KeyboardInterrupt:
    pass
