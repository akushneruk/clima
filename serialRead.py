 #!/usr/bin/env python3
import time
import serial
import re

ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

def readSerial(x):
    pattern = r"\w\w\d"
    if re.match(pattern, str(x)):
            print("Found -- "+x)
    return x

while True:
    try:
        serialLine = ser.readline().decode('utf-8')
        readSerial(serialLine)
    except:
        pass