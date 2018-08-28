#!/usr/bin/env python3

import time
import sys
import datetime
from influxdb import InfluxDBClient
from Adafruit_SHT31 import *

sensorIn = SHT31(address = 0x44)
sensorOut = SHT31(address = 0x45)

degreesIn = sensorIn.read_temperature()
humidityIn = sensorIn.read_humidity()

degreesOut = sensorOut.read_temperature()
humidityOut = sensorOut.read_humidity()

# Set this variables, influxDB should be localhost on Pi
host = "localhost"
port = 8086
user = "root"
password = "root"
dbname = "clima"

# Sample period (s)
interval = 60
measurement = "Sensor"

# Create the Influx DB object
client = InfluxDBClient(host, port, user, password, dbname)

# Run until keyboard out
try:
    while True:
        iso = time.ctime()
        print(iso)
        json_body = [
        {
          "measurement": measurement,
              "time": iso,
              "fields": {
                  "TempIn" : degreesIn,
                  "HumIn" : humidityIn,
                  "TempOut" : degreesOut,
                  "HumInOut" : humidityOut
              }
          }
        ]
 
        # Write JSON to InfluxDB
        client.write_points(json_body)
        # Wait for next sample
        time.sleep(interval)
except KeyboardInterrupt:
    pass