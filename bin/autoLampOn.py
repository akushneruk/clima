#!/usr/bin/env python3
import os
import datetime
import schedule
import time
import RPi.GPIO as GPIO


lamp_relay = 6
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(lamp_relay, GPIO.OUT, initial=1)

GPIO.output(lamp_relay, 1)

def autoLampMode(lamp_relay):
    with open("current_lamp_mode", 'r+') as file:
        for line in file:
            lamp = line
        file.seek(0)
    if lamp == "lt0":
        GPIO.output(lamp_relay, 0)
        print("lamp is on")
        time.sleep(300)
        GPIO.output(lamp_relay, 1)
        print("lamp is off")
    return

schedule.every().day.at("00:00").do(autoLampMode, lamp_relay)

try:
    while True:
        schedule.run_pending()
except KeyboardInterrupt:
    pass