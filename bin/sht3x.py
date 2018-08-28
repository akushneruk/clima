#!/usr/bin/env python3

import os
import time
import sys
import datetime
from influxdb import InfluxDBClient
from Adafruit_SHT31 import *

sensorIn = SHT31(address = 0x44)
sensorOut = SHT31(address = 0x45)

def writeData(temperature, humidity, device):
    iso = time.ctime()
    json_body = [
    {
        "measurement": device,
            "time": iso,
            "fields": {
                "Temperature" : temperature,
                "Humidity" : humidity
            }
        }
    ]

    client = InfluxDBClient("localhost", 8086, "admin", os.environ.get('INFLUXDBPWD'), "clima")
    client.write_points(json_body)
    time.sleep(60)

try:
    while True:
        degreesIn = sensorIn.read_temperature()
        humidityIn = sensorIn.read_humidity()
        writeData(degreesIn, humidityIn, "SensoreInBox")

        degreesOut = sensorOut.read_temperature()
        humidityOut = sensorOut.read_humidity()
        writeData(degreesOut, humidityOut, "SensoreOutBox")

except KeyboardInterrupt:
    pass