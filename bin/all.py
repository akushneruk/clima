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
        hum_mode.write("vt4")
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
        #print("write -- "+x)
    elif x == "lt1":
        lamp_mode.seek(0)
        lamp_mode.truncate()
        lamp_mode.write(x)
        lamp_mode.close()
        #print("write -- "+x)
    elif x == "lt2":
        lamp_mode.seek(0)
        lamp_mode.truncate()
        lamp_mode.write(x)
        lamp_mode.close()
        #print("write -- "+x)

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
        #print("hy0")
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
        #print("hy1")
    elif x == "hy2":
        GPIO.output(hum_relay, 1)
        nx_setValue(ser, 6,10,0)
        nx_setValue(ser, 4, 1, 0)
        nx_setValue(ser, 4, 2, 0)
        nx_setValue(ser, 4, 3, 1)
        #print("hy2")

def lampMode(lamp_relay, x):
    if x == "lt1":
        GPIO.output(lamp_relay, 0)
        time.sleep(10)
        GPIO.output(lamp_relay, 1)
        lamp_mode = open("current_lamp_mode", "w+")
        lamp_mode.seek(0)
        lamp_mode.truncate()
        lamp_mode.write("lt2")
        lamp_mode.close()
        nx_setValue(ser, 5,1,0)
        nx_setValue(ser, 5,2,0)
        nx_setValue(ser, 5,3,1)

def stopLamp(lamp_relay, x):
    if x == "lt2":
        GPIO.output(lamp_relay, 1)

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