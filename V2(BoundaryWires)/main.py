# -*- coding: utf-8 -*-
"""
0,2----------2,2
|             |
|             |
|             |
|             |
0,0----------2,0

        North

West            East

        South

counterclocwise rotation is negative

"""
from matplotlib.cbook import contiguous_regions
import scipy as sp

import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import time


ser = serial.Serial('/dev/ttyACM0')
print(ser.name)

