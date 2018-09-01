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

pattern = r"\w\w\d"

try:
    while 1:
        x = ser.readline().decode('utf-8')
        if re.match(pattern, str(x)):
                print("Found -- "+str(x))
        time.sleep(1)
except:
    pass
