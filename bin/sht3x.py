#!/usr/bin/env python3

import os
import time
import sys
import datetime
from influxdb import InfluxDBClient
from Adafruit_SHT31 import *

sensorIn = SHT31(address = 0x44)
sensorOut = SHT31(address = 0x45)
delay=60

def writeData():
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
        writeData()
        time.sleep(delay)
except KeyboardInterrupt:
    pass