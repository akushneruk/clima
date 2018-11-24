#!/usr/bin/env python3
import os
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

# delay for loop sleep
delay=1
# Gpio number for hum and lamp relay
hum_relay = 13
lamp_relay = 26
# Setup hum and lamp relay for output
GPIO.setup(hum_relay, GPIO.OUT, initial=1)
GPIO.setup(lamp_relay, GPIO.OUT, initial=1)
# Read temp and hum from sensors
sensorIn = SHT31(address = 0x44)
sensorOut = SHT31(address = 0x45)

firstHumStart()
firstLampStart()

try:
    while True:
        # send to screen temperature and humidity for display
        try:
            nx_setText(ser, 1,1,str(int(sensorIn.read_temperature())))
            nx_setText(ser, 1,2,str(int(sensorIn.read_humidity())))
            nx_setText(ser, 1,8,str(int(sensorOut.read_temperature())))
            nx_setText(ser, 1,9,str(int(sensorOut.read_humidity())))
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

        # Read file with current hum mode and set gpio
        with open("current_hum_mode", 'r+') as file:
            for line in file:
                mode = line
            file.seek(0)
        try:
            humMode(hum_relay, mode, int(sensorIn.read_humidity()))
        except IOError:
            pass

        # Read file with current lamp mode and set gpio
        with open("current_lamp_mode", 'r+') as file:
            for line in file:
                lamp = line
            file.seek(0)
        lampMode(lamp_relay, lamp)
        
        #
        sendStatus()
        currentTime()
        time.sleep(delay)
except KeyboardInterrupt:
    pass
