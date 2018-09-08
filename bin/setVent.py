#!/usr/bin/env python3
import time
import serial
import sys
import RPi.GPIO as GPIO
from Adafruit_SHT31 import *
from all import *

#---INIT--
vent_relay = 6
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(vent_relay, GPIO.OUT, initial=1)

sensorIn = SHT31(address = 0x44)

def gpio(value):
    GPIO.output(6, value)

def fan_thread():
    current_mode_activated = None
    current_value = None
    current_mode = None
    while True:
        time.sleep(1)
        # read file and get current vent mode( set from display)
        with open("current_vent_mode", 'r+') as file:
            for line in file:
                mode = line  # get and set  mode
            file.seek(0)
        print(mode)
        if mode != current_mode:
            current_mode = mode
            current_mode_activated = int(time.time())
        modes = {
            'vt4': [1, 1, 10, 10],  # off
            'vt2':  [0, 0, 10, 10], # on
            'vt0': [0, 1, 4, 16],   # 10/40
            'vt1': [0, 1, 4, 8],    # 10/20
            'test': [0, 1, 2, 4],   # for test
        }
        config = modes[mode]
        elapsed = (int(time.time()) - current_mode_activated) % (config[3] + config[2])
        value = config[0] if elapsed < config[2] else config[1]
        if current_value != value:
            current_value = value
            if value == 0:
                gpio(value)
                nx_setValue(ser, 6,10,0)
            elif value == 1:
                gpio(value)
                nx_setValue(ser, 6,10,1)

try:
    firstVentStart(sensorIn.read_temperature())
except IOError:
    pass

try:
    fan_thread()
except KeyboardInterrupt:
    print('interrupted!')
