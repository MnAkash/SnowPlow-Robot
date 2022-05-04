# -*- coding: utf-8 -*-
"""
0,2----------2,2
|             |
|             |
|             |
|             |
0,0----------2,0

"""

from math import pow,sqrt
from scipy.optimize import minimize
import ScanUtility
import bluetooth._bluetooth as bluez

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import time

class Beacon:
    def __init__(self) -> None:
        self.Measured_Power = -69; #RSSI power at 1 Meter distant. Needs to ba found first.
        self.N = 2; #calibration constants. Depends on the Environmental factor. Range 2–4, low to-high strength as explained above
        self.dev_id = 0#Set bluetooth device. Default 0.
        self.locations = [(0,0), (2,0), (2,2), (0,2)]
        self.distances = ''

        self.beacon_list = ["dd:34:02:05:60:13", "dd:34:02:05:62:08", "dd:34:02:05:61:75", "dd:33:0a:11:19:fa"]
        self.beaconData = [{"macAdd":"dd:34:02:05:60:13", "loc":[0,0], "dist":1.3},
                            {"macAdd":"dd:34:02:05:62:08", "loc":[2,0], "dist":1.1},
                            {"macAdd":"dd:34:02:05:61:75", "loc":[2,2], "dist":1},
                            {"macAdd":"dd:33:0a:11:19:fa", "loc":[0,2], "dist":1}]



        try:
            self.sock = bluez.hci_open_dev(self.dev_id)
            print ("\n *** Looking for BLE Beacons ***\n")
            print ("\n *** CTRL-C to Cancel ***\n")
        except:
            print ("Error accessing bluetooth")

        ScanUtility.hci_enable_le_scan(self.sock)


    def mse(self, x, beaconData):
        # Mean Square Error
        # locations: [ (lat1, long1), ... ]
        # distances: [ distance1, ... ]
        mse = 0.0
        
        for b in beaconData:
            distance_calculated = self.great_circle_distance(x[0], x[1], b["loc"][0], b["loc"][1])
            mse += pow(distance_calculated -  b["dist"], 2.0)
        return mse / len(beaconData)

    def position_estimate(self, beaconData, initial_location=[1,1]):
        # initial_location: (lat, long)
        # locations: [ (lat1, long1), ... ]
        # distances: [ distance1,     ... ]
        result = minimize(
            self.mse,                         # The error function
            initial_location,            # The initial guess
            args=(beaconData), # Additional parameters for mse
            method='L-BFGS-B',           # The optimisation algorithm
            options={
                'ftol':1e-5,         # Tolerance
                'maxiter': 1e+7      # Maximum iterations
            })
        location = result.x
        return location

    def great_circle_distance(self, x1,y1, x2, y2):
        return sqrt( (x2 - x1 )**2 + (y2-y1)**2 )
        
    def rssi2dist(self, RSSI):
        return pow(10, ((self.Measured_Power - RSSI)/(float)(10*self.N)) );


    def get_location_estimate(self):
        unique_mac_address = [] #all receieved unique beacon list to store
        try:
            while len(unique_mac_address)<len(self.beacon_list)+1:
                returnedList = ScanUtility.parse_events(self.sock, 10)
                for item in returnedList:
                    macAdd = item["macAddress"]
                    
                    if macAdd in self.beacon_list:
                        #append it in a list to filer all uniques beacon data received
                        unique_mac_address.append(macAdd)
                        #removing duplicate mac address
                        unique_mac_address = list(set(unique_mac_address))

                        #calculate distance value
                        new_distance = self.rssi2dist(item["rssi"])
                        
                        #Update distance data to beaconData dictionary accordingly
                        for i in range(len(self.beaconData)):
                            if self.beaconData[i]["macAdd"] == macAdd:
                                self.beaconData[i]["dist"] = new_distance
                        
                    
                estimated_loc = self.position_estimate(self.beaconData)
                print(estimated_loc)
                
                return estimated_loc

        except Exception as e:
            print(e)
            return [None, None]

'''
fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(-2, 6), ylim=(-2, 5))

beacon_locs, = ax.plot([], [], 'bo', label='beacons',linewidth=2, markersize=20)#blue circle
estimated_locs, = ax.plot([], [], 'ro', label='robot', linewidth=2)#red circle


bcn = Beacon()

def init():
    """initialize animation"""
    beacon_locs.set_data([], [])
    estimated_locs.set_data([], [])

    return beacon_locs, estimated_locs

def animate(i):
    """perform animation step"""
    global bcn
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
    
    return beacon_locs, estimated_locs





#estimated_loc = b.get_location_estimate()
# b.beaconData[0]['dist'] = 1.7
# b.get_location_estimate()


t0 = time()
animate(0)
t1 = time()
interval = (t1 - t0)
ani = animation.FuncAnimation(fig, animate, frames=300,
                              interval=200, blit=True, init_func=init)

plt.show()       


# plt.title('Localisation')
# plt.scatter(estimated_loc[0],estimated_loc[1],color='r', s=100)

'''