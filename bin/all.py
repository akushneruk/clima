import os
import time
import datetime
import struct
import re
import serial
import RPi.GPIO as GPIO
from influxdb import InfluxDBClient
from Adafruit_SHT31 import *

ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

def firstHumStart():
    hum_mode = open("current_hum_mode", "w+")
    hum_mode.seek(0)
    hum_mode.truncate()
    hum_mode.write("hy0")
    hum_mode.close()
    nx_setValue(ser, 4,1,1)
    nx_setValue(ser, 4,2,0)
    nx_setValue(ser, 4,3,0)

def firstVentStart(t):
    hum_mode = open("current_vent_mode", "w+")
    hum_mode.seek(0)
    hum_mode.truncate()
    if t >= 16:
        hum_mode.write("vt4")
        hum_mode.close()
        nx_setValue(ser, 2,1,0)
        nx_setValue(ser, 2,2,0)
        nx_setValue(ser, 2,3,0)
        nx_setValue(ser, 2,4,1)
    elif t < 16:
        hum_mode.write("vt1")
        hum_mode.close()
        nx_setValue(ser, 2,1,0)
        nx_setValue(ser, 2,2,1)
        nx_setValue(ser, 2,3,0)
        nx_setValue(ser, 2,4,0)

def firstLampStart():
    lamp_mode = open("current_lamp_mode", "w+")
    lamp_mode.seek(0)
    lamp_mode.truncate()
    lamp_mode.write("lt0")
    lamp_mode.close()
    nx_setValue(ser, 5,1,1)
    nx_setValue(ser, 5,2,0)
    nx_setValue(ser, 5,3,0)

def readVentMode(x):
    vent_mode = open("current_vent_mode", "w+")
    if x == "vt0":
        vent_mode.seek(0)
        vent_mode.truncate()
        vent_mode.write(x)
        vent_mode.close()
    elif x == "vt1":
        vent_mode.seek(0)
        vent_mode.truncate()
        vent_mode.write(x)
        vent_mode.close()
    elif x == "vt2":
        vent_mode.seek(0)
        vent_mode.truncate()
        vent_mode.write(x)
        vent_mode.close()
    elif x == "vt4":
        vent_mode.seek(0)
        vent_mode.truncate()
        vent_mode.write(x)
        vent_mode.close()

def readHumMode(x):
    hum_mode = open("current_hum_mode", "w+")
    if x == "hy0":
        hum_mode.seek(0)
        hum_mode.truncate()
        hum_mode.write(x)
        hum_mode.close()
    elif x == "hy1":
        hum_mode.seek(0)
        hum_mode.truncate()
        hum_mode.write(x)
        hum_mode.close()
    elif x == "hy2":
        hum_mode.seek(0)
        hum_mode.truncate()
        hum_mode.write(x)
        hum_mode.close()

def readLampMode(x):
    lamp_mode = open("current_lamp_mode", "w+")
    if x == "lt0":
        lamp_mode.seek(0)
        lamp_mode.truncate()
        lamp_mode.write(x)
        lamp_mode.close()
    elif x == "lt1":
        lamp_mode.seek(0)
        lamp_mode.truncate()
        lamp_mode.write(x)
        lamp_mode.close()
    elif x == "lt2":
        lamp_mode.seek(0)
        lamp_mode.truncate()
        lamp_mode.write(x)
        lamp_mode.close()

def humMode(hum_relay, x, hum):
    if x == "hy0":
        if hum <= 65:
            GPIO.output(hum_relay, 1)
            nx_setValue(ser, 6,10,0)
        elif hum > 65:
            GPIO.output(hum_relay, 0)
            nx_setValue(ser, 6,10,1)
        nx_setValue(ser, 4, 1, 1)
        nx_setValue(ser, 4, 2, 0)
        nx_setValue(ser, 4, 3, 0)
    elif x == "hy1":
        if hum < 80:
            GPIO.output(hum_relay, 1)
            nx_setValue(ser, 6,10,1)
        elif hum > 80:
            GPIO.output(hum_relay, 0)
            nx_setValue(ser, 6,10,1)
        nx_setValue(ser, 4, 1, 0)
        nx_setValue(ser, 4, 2, 1)
        nx_setValue(ser, 4, 3, 0)
    elif x == "hy2":
        GPIO.output(hum_relay, 1)
        nx_setValue(ser, 6,10,0)
        nx_setValue(ser, 4, 1, 0)
        nx_setValue(ser, 4, 2, 0)
        nx_setValue(ser, 4, 3, 1)

def lampMode(lamp_relay, x):
    if x == "lt1":
        GPIO.output(lamp_relay, 0)
        lamp_mode = open("manual_lamp_mode", "w+")
        lamp_mode.seek(0)
        lamp_mode.truncate()
        lamp_mode.write("on")
        lamp_mode.close()
    elif x == "lt2":
        GPIO.output(lamp_relay, 1)

def sendStatus():
    with open("current_hum_mode", 'r+') as file:
        for line in file:
            mode = line
        file.seek(0)
    if mode == "hy0":
        nx_setValue(ser, 4, 1, 1)
        nx_setValue(ser, 4, 2, 0)
        nx_setValue(ser, 4, 3, 0)
        nx_setText(ser, 6,13,"hy0")
    elif mode == "hy1":
        nx_setValue(ser, 4, 1, 0)
        nx_setValue(ser, 4, 2, 1)
        nx_setValue(ser, 4, 3, 0)
        nx_setText(ser, 6,13,"hy1")
    elif mode == "hy2":
        nx_setValue(ser, 4, 1, 0)
        nx_setValue(ser, 4, 2, 0)
        nx_setValue(ser, 4, 3, 1)
        nx_setText(ser, 6,13,"hy2")

    with open("current_vent_mode", 'r+') as file:
        for line in file:
            mode = line
        file.seek(0)
    if mode == "vt0":
        nx_setValue(ser, 2,1,1)
        nx_setValue(ser, 2,2,0)
        nx_setValue(ser, 2,3,0)
        nx_setValue(ser, 2,4,0)
        nx_setText(ser, 6,12,"vt0")
    elif mode == "vt1":
        nx_setValue(ser, 2,1,0)
        nx_setValue(ser, 2,2,1)
        nx_setValue(ser, 2,3,0)
        nx_setValue(ser, 2,4,0)
        nx_setText(ser, 6,12,"vt1")
    elif mode == "vt2":
        nx_setValue(ser, 2,1,0)
        nx_setValue(ser, 2,2,0)
        nx_setValue(ser, 2,3,1)
        nx_setValue(ser, 2,4,0)
        nx_setText(ser, 6,12,"vt2")
    elif mode == "vt4":
        nx_setValue(ser, 2,1,0)
        nx_setValue(ser, 2,2,0)
        nx_setValue(ser, 2,3,0)
        nx_setValue(ser, 2,4,1)
        nx_setText(ser, 6,12,"vt4")
        
    with open("current_lamp_mode", 'r+') as file:
        for line in file:
            mode = line
        file.seek(0)
    if mode == "lt0":
        nx_setValue(ser, 5,1,1)
        nx_setValue(ser, 5,2,0)
        nx_setValue(ser, 5,3,0)
        nx_setText(ser, 6,14,"lt0")
    elif mode == "lt1":
        nx_setValue(ser, 5,1,0)
        nx_setValue(ser, 5,2,1)
        nx_setValue(ser, 5,3,0)   
        nx_setText(ser, 6,14,"lt1")
    elif mode == "lt2":
        nx_setValue(ser, 5,1,0)
        nx_setValue(ser, 5,2,0)
        nx_setValue(ser, 5,3,1)     
        nx_setText(ser, 6,14,"lt2")

    status = open("status", "w+")
    status.seek(0)
    status.truncate()
    status.write("0")
    status.close()  

def writeData(tempIn, humIn, tempOut, humOut ):
    """ write all data to db """
    json_body_in = [
    {
        "measurement": "SensoreInBox",
            "fields": {
                "Temperature" : tempIn,
                "Humidity" : humIn
            }
        }
    ]

    json_body_out = [
    {
        "measurement": "SensoreOutBox",
            "fields": {
                "Temperature" : tempOut,
                "Humidity" : humOut
            }
        }
    ]

    client = InfluxDBClient("localhost", 8086, "admin", os.environ.get('INFLUXDBPWD'), "clima")
    client.write_points(json_body_in)
    client.write_points(json_body_out)

def nx_setText(ser, pageID, componentID, text):  # writes the text in the text component atribute .txt
    EndCom = "\xff\xff\xff"
    text = 'p[' + str(pageID) + '].b[' + str(componentID)+']''.txt="' + text + '"'
    ser.write((text+EndCom).encode('latin-1'))
    return None

def nx_getValue(ser, pageID, componentID):  # Returns the .val from a component in a page as text
    EndCom = "\xff\xff\xff"
    send = 'get ' + 'p[' + str(pageID) + '].b[' + str(componentID)+']'+'.val'
    ser.write((send+EndCom).encode('latin-1'))
    value=ser.read_until(EndCom)
    try:
        if hex(value[0]) == '0x71':
            value = value[1]+value[2]*256+value[3]*65536+value[4]*16777216 # little endian
            return value  # as float
    except:
        pass

def nx_setValue(ser, pageID, componentID, value):  # writes the value in the number component atribute .val
    EndCom = "\xff\xff\xff"
    value_str = 'p[' + str(pageID) + '].b[' + str(componentID)+']''.val=' + str(value)  # test here the "'"
    ser.write((value_str+EndCom).encode('latin-1'))
    return None