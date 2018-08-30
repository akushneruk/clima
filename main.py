#!/usr/bin/env python3

import threading
import time
import sys

mode = "off"


def gpio(value):
  print "gpio: ", value
  sys.stdout.flush()

def fan_thread():
    current_mode_activated = None
    current_value = None
    current_mode = None
    global mode
    while True:
        time.sleep(1)
        if mode != current_mode:
            current_mode = mode
            current_mode_activated = int(time.time())
        modes = {
            'off': [0, 0, 10, 10],
            'on':  [1, 1, 10, 10],
            '10/40': [1, 0, 600, 3000],
            '10/20': [1, 0, 600, 1200],
            'test': [1, 0, 3, 10],
        }
        config = modes[mode]
        elapsed = (int(time.time()) - current_mode_activated) % config[3]
        value = config[0] if elapsed < config[2] else config[1]
        if current_value != value:
            gpio(value)

fan = threading.Thread(name='fan', target=fan_thread)
fan.start()

mode = "test"
fan.join()

