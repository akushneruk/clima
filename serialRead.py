#!/usr/bin/env python3
import time
import serial
import re

ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

fo = open("current_vent_mode", "w+")

def readSerial(x):
    pattern = r"\w\w\d"
    mode=""
    if re.match(pattern, str(x)):
        if x == "vt0":
            fo.seek(0)
            fo.truncate()
            fo.write(x)
            print("write -- "+x)
        elif x == "vt1":
            fo.seek(0)
            fo.truncate()
            fo.write(x)
            print("write -- "+x)
        elif x == "vt2":
            fo.seek(0)
            fo.truncate()
            fo.write(x)
            print("write -- "+x)
        elif x == "vt4":
            fo.seek(0)
            fo.truncate()
            fo.write(x)
            print("write -- "+x)
        else:
            print("suck")

while True:
    serialLine = ser.readline().decode('latin-1')
    readSerial(serialLine)
    time.sleep(1)
