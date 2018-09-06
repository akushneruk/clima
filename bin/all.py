import os
import time
import datetime
import struct
import re
import serial
import RPi.GPIO as GPIO
from influxdb import InfluxDBClient
from Adafruit_SHT31 import *

def gpio(hum_relay, value):
    GPIO.output(hum_relay, value)

def readVentMode(x):
    vent_mode = open("current_vent_mode", "w+")
    if x == "vt0":
        vent_mode.seek(0)
        vent_mode.truncate()
        vent_mode.write(x)
        vent_mode.close()
        #print("write -- "+x)
    elif x == "vt1":
        vent_mode.seek(0)
        vent_mode.truncate()
        vent_mode.write(x)
        vent_mode.close()
        #print("write -- "+x)
    elif x == "vt2":
        vent_mode.seek(0)
        vent_mode.truncate()
        vent_mode.write(x)
        vent_mode.close()
        #print("write -- "+x)
    elif x == "vt4":
        vent_mode.seek(0)
        vent_mode.truncate()
        vent_mode.write(x)
        vent_mode.close()
        #print("write -- "+x)

def readHumMode(x):
    hum_mode = open("current_hum_mode", "w+")
    if x == "hy0":
        hum_mode.seek(0)
        hum_mode.truncate()
        hum_mode.write(x)
        hum_mode.close()
        #print("write -- "+x)
    elif x == "hy1":
        hum_mode.seek(0)
        hum_mode.truncate()
        hum_mode.write(x)
        hum_mode.close()
        #print("write -- "+x)
    elif x == "hy2":
        hum_mode.seek(0)
        hum_mode.truncate()
        hum_mode.write(x)
        hum_mode.close()
        #print("write -- "+x)

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
            gpio(hum_relay, 1)
        elif hum > 65:
            gpio(hum_relay, 0)
        nx_setValue(ser, 4, 1, 1)
        nx_setValue(ser, 4, 2, 0)
        nx_setValue(ser, 4, 3, 0)
        #print("hy0")
    elif x == "hy1":
        if hum < 80:
            gpio(hum_relay, 1)
        elif hum > 80:
            gpio(hum_relay, 0)
        nx_setValue(ser, 4, 1, 0)
        nx_setValue(ser, 4, 2, 1)
        nx_setValue(ser, 4, 3, 0)
        #print("hy1")
    elif x == "hy2":
        gpio(hum_relay, 1)
        nx_setValue(ser, 4, 1, 0)
        nx_setValue(ser, 4, 2, 0)
        nx_setValue(ser, 4, 3, 1)
        #print("hy2")


def writeData(tempIn, humIn, tempOut, humOut ):
    """ write all data to db """
    iso = time.ctime()
    json_body_in = [
    {
        "measurement": "SensoreInBox",
            "time": iso,
            "fields": {
                "Temperature" : tempIn,
                "Humidity" : humIn
            }
        }
    ]

    json_body_out = [
    {
        "measurement": "SensoreOutBox",
            "time": iso,
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