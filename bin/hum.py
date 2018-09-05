#!/usr/bin/env python3
import time
import serial
import sys
from Adafruit_SHT31 import *
import RPi.GPIO as GPIO

relay = 13
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(relay, GPIO.OUT, initial=0)

sensor = SHT31(address = 0x44)

ser = serial.Serial(
 port='/dev/ttyAMA0',
 baudrate = 9600,
 parity=serial.PARITY_NONE,
 stopbits=serial.STOPBITS_ONE,
 bytesize=serial.EIGHTBITS,
 timeout=1
)

def nx_setValue(ser, pageID, componentID, value):  # writes the value in the number component atribute .val
    EndCom = "\xff\xff\xff"
    value_str = 'p[' + str(pageID) + '].b[' + str(componentID)+']''.val=' + str(value)  # test here the "'"
    ser.write((value_str+EndCom).encode('latin-1'))
    return None

def gpio(value):
    GPIO.output(relay, value)

def hum(x, hum):
    if x == "hy0":
        if hum <= 65:
            gpio(1)
        elif hum > 65:
            gpio(0)
        nx_setValue(ser, 4, 1, 1)
        nx_setValue(ser, 4, 2, 0)
        nx_setValue(ser, 4, 3, 0)
        #print("hy0")
    elif x == "hy1":
        if hum < 80:
            gpio(1)
        elif hum > 80:
            gpio(0)
        nx_setValue(ser, 4, 1, 0)
        nx_setValue(ser, 4, 2, 1)
        nx_setValue(ser, 4, 3, 0)
        #print("hy1")
    elif x == "hy2":
        gpio(1)
        nx_setValue(ser, 4, 1, 0)
        nx_setValue(ser, 4, 2, 0)
        nx_setValue(ser, 4, 3, 1)
        #print("hy2")

try:
    while True:
        try:
            humidity = sensor.read_humidity()
        except IOError:
            print("Suck with sensors")
        with open("current_hum_mode", 'r+') as file:
            for line in file:
                mode = line
            file.seek(0)
        hum(mode, int(humidity))
        time.sleep(1)
except KeyboardInterrupt:
    print('interrupted!')