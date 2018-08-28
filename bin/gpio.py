#!/usr/bin/env python3

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
channel_1 = 6
channel_2 = 13
channel_3 = 19
channel_4 = 26


GPIO.setup(channel_1, GPIO.OUT)
GPIO.setup(channel_2, GPIO.OUT)
GPIO.setup(channel_3, GPIO.OUT)
GPIO.setup(channel_4, GPIO.OUT)

# Setup your channel
#GPIO.setup(channel, GPIO.OUT)
#GPIO.output(channel, GPIO.LOW)

# To test the value of a pin use the .input method
channel_is_on = GPIO.input(channel_1)  # Returns 0 if OFF or 1 if ON
print(channel_is_on)
channel_is_on = GPIO.input(channel_2)
print(channel_is_on)
channel_is_on = GPIO.input(channel_3)
print(channel_is_on)
channel_is_on = GPIO.input(channel_4)
print(channel_is_on)
