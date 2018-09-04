import sys
import time
import serial
import struct
import re
import RPi.GPIO as GPIO

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

#nx_setcmd_0par(ser, 'rest')
#nx_setText(ser, 2,4,"val=1")

nx_setValue(ser, 2,1,0)
nx_setValue(ser, 2,2,0)
nx_setValue(ser, 2,3,0)
nx_setValue(ser, 2,4,1)