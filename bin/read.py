#!/usr/bin/env python3
import os
import time
import time
import datetime
import struct
import re
import serial
import RPi.GPIO as GPIO
from influxdb import InfluxDBClient
from Adafruit_SHT31 import *
from all import *

ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
ser.reset_output_buffer()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# channel = [6, 13, 19, 26]

# def intiGpio(channel):
#     for index in range(len(channel)):
#         GPIO.setup(channel[index], GPIO.OUT, initial=1)
#         index+= 1

hum_relay = 13
sensorIn = SHT31(address = 0x44)
sensorOut = SHT31(address = 0x45)
delay=1
GPIO.setup(13, GPIO.OUT, initial=1)

try:
    while True:
        # send to influxdb set temperature and humidity for display
        try:
            nx_setText(ser, 1,1,str(int(sensorIn.read_temperature())))
            nx_setText(ser, 1,2,str(int(sensorIn.read_humidity())))
            writeData( sensorIn.read_temperature(), sensorIn.read_humidity(), sensorOut.read_temperature(), sensorOut.read_humidity() )
        except IOError:
            pass
        
        # Wait for incoming serial and write to file new mode
        serialLine = ser.readline().decode('latin-1')
        if re.match(r"v\w\d", str(serialLine)):
            readVentMode(serialLine)
        elif re.match(r"h\w\d", str(serialLine)):
            readHumMode(serialLine)
        elif re.match(r"l\w\d", str(serialLine)):
            readLampMode(serialLine)

        #
        with open("current_hum_mode", 'r+') as file:
            for line in file:
                mode = line
            file.seek(0)
        try:
            humMode(hum_relay, mode, int(sensorIn.read_temperature()))
        except IOError:
            pass

        time.sleep(delay)
except KeyboardInterrupt:
    pass
