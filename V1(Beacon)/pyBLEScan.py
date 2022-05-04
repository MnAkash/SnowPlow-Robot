# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 23:42:30 2022

@author: akash
"""

#This is a working prototype. DO NOT USE IT IN LIVE PROJECTS

import ScanUtility
import bluetooth._bluetooth as bluez

#Set bluetooth device. Default 0.
dev_id = 0
try:
	sock = bluez.hci_open_dev(dev_id)
	print ("\n *** Looking for BLE Beacons ***\n")
	print ("\n *** CTRL-C to Cancel ***\n")
except:
	print ("Error accessing bluetooth")

ScanUtility.hci_enable_le_scan(sock)
#Scans for iBeacons

def rssi2dist(RSSI):
    return pow(10, ((Measured_Power - RSSI)/(float)(10*N)) )


Measured_Power = -53; #RSSI power at 1 Meter distant. Needs to ba found first.
N = 2; #calibration constants. Depends on the Environmental factor. Range 2–4, low to-high strength as explained above


#beacon_list = ["dd:34:02:05:60:13", "dd:34:02:05:62:08", "dd:34:02:05:61:75", "dd:33:0a:11:19:fa"]
beacon_list = ["dd:34:02:05:60:13"]
try:
    while True:
        returnedList = ScanUtility.parse_events(sock, 10)
        for item in returnedList:
            if item["macAddress"] in beacon_list:
                dist = rssi2dist(item["rssi"])
                print(dist)
                #print("")
                
except KeyboardInterrupt:
    pass