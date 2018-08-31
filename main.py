#!/usr/bin/env python3

import threading
import time
import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
channel = [6, 13, 19, 26]

for index in range(len(channel)):
	GPIO.setup(channel[index], GPIO.OUT)
	index+= 1


mode = "off"


def gpio(value):
  GPIO.output(19, value)

def fan_thread():
    current_mode_activated = None
    current_value = None
    current_mode = None
    global mode
    while True:
        time.sleep(1)
        if mode != current_mode:
            current_mode = mode
            current_mode_activated = int(time.time())
        modes = {
            'off': [0, 0, 10, 10], # param1 gpio value that wait for param3 time, param2 gpio value that wait for param4 time 
            'on':  [1, 1, 10, 10],
            '10/40': [1, 0, 600, 2400],
            '10/20': [1, 0, 600, 1200],
            'test': [1, 0, 3, 10],
        }
        config = modes[mode]
        elapsed = (int(time.time()) - current_mode_activated) % (config[3] + config[2])
        value = config[0] if elapsed < config[2] else config[1]
        if current_value != value:
            current_value = value
            gpio(value)

#fan = threading.Thread(name='fan', target=fan_thread)
#fan.start()

#mode = "test"
#fan.join()
fan_thread()
