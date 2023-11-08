build_number = 16032023

#-------------------------------- User Config ---------------------------------

bridge_address = "192.168.0.6"
# transmitter_address = "ED:7E:B6:76:9C:0C"
# transmitter_address = "A0:38:F8:4C:24:97" # Oura
# transmitter_address = "04:72:95:24:36:16"
transmitter_address = "DB:90:14:18:18:20" # JUUL
connection_timeout = 3 #seconds
lock_machine = True
rssi_mode = True
rssi_limit = -79 # for when rssi_mode = True
lights = [15, 16, 17] # array of integers, blank defaults to all

#------------------------------------------------------------------------------
#--------------------------------- Packages -----------------------------------

import os
import platform
from termcolor import colored # https://pypi.org/project/termcolor/
from modules.BluetoothRunner import *
from modules.Activities import *

#---------------------------------- Preamble ------------------------------------

if transmitter_address is None:
    print("Edit the 'User Config' section of hue_beacon.py with the transmitter address.")
    raise SystemExit

print(colored("\n> Build prototype #"+str(build_number), "dark_grey"))
if platform.system() == "Windows":
    os.system("color")
    print(colored("Configured parameters for windows environment.", "dark_grey"))

print(colored("\nDeveloped by James Swift 2023", "dark_grey"))
print(colored("Latest versions and documentation available at", "dark_grey"), "https://github.com/James-2879/<repo-name>")

#---------------------------------- Script ------------------------------------

activities = Activities(bridge = bridge_address,
                        lights = lights)
bluetooth = BluetoothRunner(address = transmitter_address,
                            timeout = connection_timeout,
                            rssi_mode = rssi_mode,
                            rssi_limit = rssi_limit,
                            activities = activities)

print("\nBluetooth connection status:")
while True:
    try:
        bluetooth.runner()
    except KeyboardInterrupt:
        bluetooth.end()
        