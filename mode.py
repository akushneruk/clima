import sys
import time
import serial
import struct
import RPi.GPIO as GPIO

def intiGpio(channel):
    for index in range(len(channel)):
        GPIO.setup(channel[index], GPIO.OUT, initial=1)
        index+= 1

def gpio(value):
    GPIO.output(6, value)

def fan_thread(mode):
    current_mode_activated = None
    current_value = None
    current_mode = None  
    while True:
        time.sleep(1)
        if mode != current_mode:
            current_mode = mode
            current_mode_activated = int(time.time())
        modes = {
            'vt4': [1, 1, 10, 10], # param1 gpio value that wait for param3 time, param2 gpio value that wait for param4 time
            'vt2':  [0, 0, 10, 10], # on
            'vt0': [0, 1, 4, 16], # 10/40
            'vt1': [0, 1, 4, 8], # 10/20
            'test': [0, 1, 2, 4],
        }
        config = modes[mode]
        elapsed = (int(time.time()) - current_mode_activated) % (config[3] + config[2])
        value = config[0] if elapsed < config[2] else config[1]
        if current_value != value:
            current_value = value
            gpio(value)


def nx_setText(ser, pageID, componentID, text):  # writes the text in the text component atribute .txt
    EndCom = "\xff\xff\xff"
    text = 'p[' + str(pageID) + '].b[' + str(componentID)+']''.txt="' + text + '"'
    ser.write((text+EndCom).encode('latin-1'))
    return None
    
def nx_setcmd_0par(ser, command):  #Set operational Commands without parameters
    EndCom = "\xff\xff\xff"
    # Possible commands: 'ref_stop', 'ref_star', 'touch_j' (calibrate), 'com_stop', 'com_start', 'code_c','rest', 'doevents'
    # see instruction set of NEXTION device to know the possible commands and what they do
    ser.write((command+EndCom).encode('latin-1'))
    return None

def nx_setValue(ser, pageID, componentID, value):  # writes the value in the number component atribute .val
    EndCom = "\xff\xff\xff"
    value_str = 'p[' + str(pageID) + '].b[' + str(componentID)+']''.val=' + str(value)  # test here the "'"
    ser.write((value_str+EndCom).encode('latin-1'))
    return None