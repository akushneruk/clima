#!/usr/bin/env python3

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
channel = [6, 13, 19, 26]

for index in range(len(channel)):
    	GPIO.setup(channel[index], GPIO.OUT)
	index+= 1


