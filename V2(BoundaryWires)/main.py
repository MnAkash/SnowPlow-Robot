# -*- coding: utf-8 -*-
"""

        North

West            East

        South

counterclocwise rotation is negative

"""
import serial
import gy271compass as GY271
from time import time

compass = GY271.Compass()

with serial.Serial('/dev/ttyACM0', 19200, timeout=1) as ser:
     x = ser.read()          # read one byte
     if x == 'c':
        direction, temp = compass.reading()
        ser.write(direction)
