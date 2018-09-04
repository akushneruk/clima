#!/usr/bin/env python3

import os
import time
import sys
import datetime
import serial
import struct
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

EndCom = "\xff\xff\xff"
sensorIn = SHT31(address = 0x44)
sensorOut = SHT31(address = 0x45)
delay=10

def nx_setText(ser, pageID, componentID, text):  # writes the text in the text component atribute .txt
    text = 'p[' + str(pageID) + '].b[' + str(componentID)+']''.txt="' + text + '"'
    ser.write((text+EndCom).encode('latin-1'))
    return None

def writeData():
    """ write all data to db """
    iso = time.ctime()
    json_body_in = [
    {
        "measurement": "SensoreInBox",
            "time": iso,
            "fields": {
                "Temperature" : sensorIn.read_temperature(),
                "Humidity" : sensorIn.read_humidity()
            }
        }
    ]

    json_body_out = [
    {
        "measurement": "SensoreOutBox",
            "time": iso,
            "fields": {
                "Temperature" : sensorOut.read_temperature(),
                "Humidity" : sensorOut.read_humidity()
            }
        }
    ]

    client = InfluxDBClient("localhost", 8086, "admin", os.environ.get('INFLUXDBPWD'), "clima")
    client.write_points(json_body_in)
    client.write_points(json_body_out)

try:
    while True:
        writeData()
        # Send temp
        nx_setText(ser, 1,1,str(int(sensorIn.read_temperature())))
        # Send hum
        nx_setText(ser, 1,2,str(int(sensorIn.read_humidity())))
        time.sleep(delay)
except KeyboardInterrupt:
    pass
