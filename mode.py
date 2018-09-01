import time
import sys
import RPi.GPIO as GPIO

def intiGpio(channel):
    for index in range(len(channel)):
        GPIO.setup(channel[index], GPIO.OUT, initial=1)
        index+= 1

def gpio(value):
    GPIO.output(6, value)

def fan_thread(mode):
    current_mode_activated = None
    current_value = None
    current_mode = None  
    while True:
        time.sleep(1)
        if mode != current_mode:
            current_mode = mode
            current_mode_activated = int(time.time())
        modes = {
            'off': [1, 1, 10, 10], # param1 gpio value that wait for param3 time, param2 gpio value that wait for param4 time
            'on':  [0, 0, 10, 10],
            '10/40': [0, 1, 6, 24],
            '10/20': [0, 1, 6, 12],
            'test': [0, 1, 2, 4],
        }
        config = modes[mode]
        elapsed = (int(time.time()) - current_mode_activated) % (config[3] + config[2])
        value = config[0] if elapsed < config[2] else config[1]
        if current_value != value:
            current_value = value
            gpio(value)
