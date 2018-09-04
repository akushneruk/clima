#!/usr/bin/env python3
import time
import serial
import sys

hum_mode_pattern = r"h\w\d"

try:
    while True:
        with open("current_hum_mode", 'r+') as file:
            for line in file:
                mode = line  # get and set  mode
            file.seek(0)
        print(mode)
except KeyboardInterrupt:
    print('interrupted!')


