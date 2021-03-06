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
import gy271compass as GY271
from motor import motorControl
from beacon import Beacon


import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import time

compass = GY271.Compass()
robot = motorControl()
bcn = Beacon()

error_acceptance = 3 #degrees
X_max = 2
X_min = 0
current_dir = 'N' #can be W/S/E

def init():
    """initialize animation"""
    beacon_locs.set_data([], [])
    estimated_locs.set_data([], [])

    return beacon_locs, estimated_locs

def limitTo360(val):
    #when any angle value exceeds, it scroll back to 0 and vice versa
    if val>360:
        limited_val = val-360
    elif val<0:
        limited_val = val+360
    else:
        limited_val = val
    return limited_val

def whereToRotate(current, required):
    #returns 'left' of 'right'
    if current < required:
        if abs(current-required)<180: return 'right'
        else: return 'left'
    elif current > required:
        if abs(current-required)<180: return 'left'
        else: return 'right'
    else:
        pass

def rotateWest(speed):
    global current_dir
    bearing, _ = compass.reading()
    while( abs(bearing-west) > error_acceptance ):
        bearing, _ = compass.reading()
        if whereToRotate(bearing,west) == 'right':
            robot.right(speed)
            print("Rotating right")
        elif whereToRotate(bearing,west) == 'left':
            robot.left(speed)
            print("Rotating left")
    current_dir = 'W'
    print("Rotated to west")
    robot.brake()

def rotateEast(speed):
    global current_dir
    bearing, _ = compass.reading()
    while( abs(bearing-east) > error_acceptance ):
        bearing, _ = compass.reading()
        if whereToRotate(bearing,east) == 'right':
            robot.right(speed)
            print("Rotating right")
        elif whereToRotate(bearing,east) == 'left':
            robot.left(speed)
            print("Rotating left")
    current_dir = 'E'
    print("Rotated to east")
    robot.brake()

def rotateSouth(speed):
    global current_dir
    bearing, _ = compass.reading()
    while( abs(bearing-south) > error_acceptance ):
        bearing, _ = compass.reading()
        if whereToRotate(bearing,south) == 'right':
            robot.right(speed)
            print("Rotating right")
        elif whereToRotate(bearing,south) == 'left':
            robot.left(speed)
            print("Rotating left")
    current_dir = 'S'
    print("Rotated to south")
    robot.brake()

def rotateNorth(speed):
    global current_dir
    bearing, _ = compass.reading()
    while( abs(bearing-north) > error_acceptance ):
        bearing, _ = compass.reading()
        if whereToRotate(bearing,north) == 'right':
            robot.right(speed)
            print("Rotating right")
        elif whereToRotate(bearing,north) == 'left':
            robot.left(speed)
            print("Rotating left")
    current_dir = 'N'
    print("Rotated to north")
    robot.brake()

def moveAhead():
    #move ahead in one direction it is faced at
    global current_dir

    if current_dir   == 'E': required_bearing = east
    elif current_dir == 'W': required_bearing = west
    elif current_dir == 'N': required_bearing = north
    elif current_dir == 'S': required_bearing = south

    current_bearing, temp = compass.reading()

    if  abs(current_bearing-required_bearing) < error_acceptance:
        robot.forward(20)
######################################################################################################
    elif whereToRotate(current_bearing, required_bearing) == 'right': #if rotated too left, turn right
        while (current_bearing-required_bearing) > error_acceptance:
            robot.right(20)
            current_bearing, temp = compass.reading()
        robot.forward(20)

    elif whereToRotate(current_bearing, required_bearing) == 'left': #if rotated too right, turn left
        while (current_bearing-required_bearing) > error_acceptance:
            robot.left(20)
            current_bearing, temp = compass.reading()
        robot.forward(20)


def changeCourse():
    #change course at the end of the line
    global current_dir

    if current_dir == 'N':
        robot.backward(20)
        time.sleep(1)
        rotateWest(20)
        time.sleep(1)
        robot.forward(20)
        time.sleep(2) 
        rotateSouth(20)
        time.sleep(1)
        robot.forward(20)

    elif current_dir == 'S':
        robot.backward(20)
        time.sleep(1)
        rotateWest(20)
        time.sleep(1)
        robot.forward(20)
        time.sleep(2) 
        rotateNorth(20)
        time.sleep(1)
        robot.forward(20)

    else:
        pass

def animate(i):
    """perform animation step"""
    global bcn
    global estimated_loc

    estimated_loc = bcn.get_location_estimate()
    beaconData = bcn.beaconData
    b_x = []
    b_y = []
    for b in beaconData:
        #self.axes.add_artist(plt.Circle(b["loc"], b["dist"], color='b', fill=False))
        b_x.append(b["loc"][0])
        b_y.append(b["loc"][1])

    beacon_locs.set_data(b_x, b_y)
    estimated_locs.set_data(estimated_loc[0],estimated_loc[1])
    

    #=====move ahead in one direction it is faced at
    moveAhead()



    #==============Rotation at ends part
    if estimated_loc[0] > X_max  or estimated_loc[0] < X_min:
        changeCourse()




    return beacon_locs, estimated_locs

#######################End of FUnctions#####################################


north, temp = compass.reading()
west  = limitTo360(north + 90)
east = limitTo360(north - 90)
south  = limitTo360(north + 180)


print("North: ", north)
print("South: ", south)
print("East: ", east)
print("West: ", west)
print("Temperature",temp)


estimated_loc = (0,0)

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(-2, 6), ylim=(-2, 5))

beacon_locs, = ax.plot([], [], 'bo', label='beacons',linewidth=2, markersize=20)#blue circle
estimated_locs, = ax.plot([], [], 'ro', label='robot', linewidth=2)#red circle
'''


t0 = time()
animate(0)
t1 = time()
interval = (t1 - t0)
ani = animation.FuncAnimation(fig, animate, frames=300,interval=100, blit=True, init_func=init)
plt.show()       
'''

