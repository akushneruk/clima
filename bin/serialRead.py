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

vent_mode_pattern = r"v\w\d"
hum_mode_pattern = r"h\w\d"
lamp_mode_pattern = r"l\w\d"

def readVentMode(x):
    if x == "vt0":
        vent_mode = open("current_vent_mode", "w+")
        vent_mode.seek(0)
        vent_mode.truncate()
        vent_mode.write(x)
        vent_mode.close()
        print("write -- "+x)
    elif x == "vt1":
        vent_mode = open("current_vent_mode", "w+")
        vent_mode.seek(0)
        vent_mode.truncate()
        vent_mode.write(x)
        vent_mode.close()
        print("write -- "+x)
    elif x == "vt2":
        vent_mode = open("current_vent_mode", "w+")
        vent_mode.seek(0)
        vent_mode.truncate()
        vent_mode.write(x)
        vent_mode.close()
        print("write -- "+x)
    elif x == "vt4":
        vent_mode = open("current_vent_mode", "w+")
        vent_mode.seek(0)
        vent_mode.truncate()
        vent_mode.write(x)
        vent_mode.close()
        print("write -- "+x)
    else:
        print("suck")

def readHumMode(x):
    if x == "hy0":
        hum_mode = open("current_hum_mode", "w+")
        hum_mode.seek(0)
        hum_mode.truncate()
        hum_mode.write(x)
        hum_mode.close()
        print("write -- "+x)
    elif x == "hy1":
        hum_mode = open("current_hum_mode", "w+")
        hum_mode.seek(0)
        hum_mode.truncate()
        hum_mode.write(x)
        hum_mode.close()
        print("write -- "+x)
    elif x == "hy2":
        hum_mode = open("current_hum_mode", "w+")
        hum_mode.seek(0)
        hum_mode.truncate()
        hum_mode.write(x)
        hum_mode.close()
        print("write -- "+x)

def readLampMode(x):
    if x == "lt0":
        lamp_mode = open("current_lamp_mode", "w+")
        lamp_mode.seek(0)
        lamp_mode.truncate()
        lamp_mode.write(x)
        lamp_mode.close()
        print("write -- "+x)
    elif x == "lt1":
        lamp_mode = open("current_lamp_mode", "w+")
        lamp_mode.seek(0)
        lamp_mode.truncate()
        lamp_mode.write(x)
        lamp_mode.close()
        print("write -- "+x)
    elif x == "lt2":
        lamp_mode = open("current_lamp_mode", "w+")
        lamp_mode.seek(0)
        lamp_mode.truncate()
        lamp_mode.write(x)
        lamp_mode.close()
        print("write -- "+x)

try:
    while True:
        serialLine = ser.readline().decode('latin-1')
        if re.match(vent_mode_pattern, str(serialLine)):
            readVentMode(serialLine)
        elif re.match(hum_mode_pattern, str(serialLine)):
            readHumMode(serialLine)
        elif re.match(lamp_mode_pattern, str(serialLine)):
            readLampMode(serialLine)
except KeyboardInterrupt:
    pass
