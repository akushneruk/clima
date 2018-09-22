#!/usr/bin/env python3

import time
import datetime
from influxdb import InfluxDBClient
from Adafruit_SHT31 import *
from all import *

sensorIn = SHT31(address = 0x44)
sensorOut = SHT31(address = 0x45)
delay = 60

status = open("status", "w+")
status.seek(0)
status.truncate()
status.write("0")
status.close()

while True:
    # send to influxdb set temperature and humidity for display
    try:
        writeData( sensorIn.read_temperature(), sensorIn.read_humidity(), sensorOut.read_temperature(), sensorOut.read_humidity() )
        # treger, send all status to display
        status = open("status", "w+")
        status.seek(0)
        status.truncate()
        status.write("1")
        status.close()

        time.sleep(delay)
    except IOError:
        pass
