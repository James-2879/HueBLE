build_number = 16032023

#-------------------------------- User Config ---------------------------------

bridge_address = "192.168.0.6"
transmitter_address = "ED:7E:B6:76:9C:0C"
connection_timeout = 4 #seconds
lock_machine = False
rssi_mode = True
rssi_limit = -82 #for when rssi_mode = True
lights = [15, 16] #array of integers, blank defaults to all

#------------------------------------------------------------------------------
#--------------------------------- Packages -----------------------------------

import os
import ctypes
import asyncio
import platform

from termcolor import colored
from bleak import BleakScanner
from hue_api import HueApi

# https://pypi.org/project/termcolor/
# https://bleak.readthedocs.io/en/latest/api/scanner.html
# http://hue-py-docs.s3-website-us-east-1.amazonaws.com/index.html

#-------------------------------- Definitions --------------------------------

connection_statistics = dict(connected = 0, disconnected = 0, rssi_limit = 0)
connection_attempts = 0
api = HueApi() # instantiate class
loop = asyncio.new_event_loop() # create loop for BLE detection
asyncio.set_event_loop(loop)

#---------------------------------- Methods -----------------------------------

class BLE_HUE:        
    def __init__(self, address, timeout):
        self.address = address
        self.timeout = timeout
    
    async def search_for_device(self):
        return_var = await BleakScanner.find_device_by_address(self.address, self.timeout)
        return(return_var)

    def async_function(self):
        loop = asyncio.get_event_loop()
        return_var = loop.run_until_complete(self.search_for_device())
        return(return_var)
    
    def ble_detection(self):
        transmitter_status = self.async_function()
        try:
            UTILS.clear_terminal()
            print(colored("[OK]", "green"), transmitter_status, "RSSI:", transmitter_status.rssi, colored("Detected", "green"), end = "\r")
            global connection_attempts
            connection_attempts = 0
            if rssi_mode == True:
                if transmitter_status.rssi < rssi_limit:
                    self.update_connection_statistics("rssi_limit")
                    self.out_of_range("rssi_limit")
                else:
                    self.update_connection_statistics("connected")
                    api.turn_on(lights)
            else:
                self.update_connection_statistics("connected")
                api.turn_on(lights)
        except AttributeError:
            self.update_connection_statistics("disconnected")
            self.out_of_range("disconnected")
    
    @staticmethod        
    def out_of_range(reason):
        global connection_attempts
        connection_attempts += 1
        if reason == "disconnected":
            UTILS.clear_terminal()
            print(colored("[!!]", "red"), connection_attempts, "failed connection attempts", colored("Disconnected", "red"), end = "\r")
        elif reason == "rssi_limit":
            UTILS.clear_terminal()
            print(colored("[!!]", "red"), connection_attempts, "failed connection attempts", colored("RSSI limit", "yellow"), end = "\r")
        if connection_attempts == 3:
            api.turn_off(indices = lights)
            UTILS.lock_workstation()
            
    @staticmethod
    def update_connection_statistics(event):
        connection_statistics[event] += 1
    
class UTILS:
    @staticmethod
    def lock_workstation():
        if platform.system == "Windows":
            ctypes.windll.user32.LockWorkStation()
    
    @staticmethod        
    def clear_terminal():
        print("                                                                        ", end = "\r")

#---------------------------------- Script ------------------------------------
### Config ###

print(colored("\n> Build prototype #"+str(build_number), "dark_grey"))

if platform.system() == "Windows":
    os.system("color")
    print(colored("Configured parameters for windows environment.", "dark_grey"))

### Messages ###

print(colored("\nDeveloped by James Swift 2023", "dark_grey"))
print(colored("Latest versions and documentation available at", "dark_grey"), "https://github.com/James-2879/<repo-name>")
# print(colored("To support future development, feel free to buy me a coffee at", "dark_grey"), "https://paypal.me/<user> ;)")

### Script ###

# connect to Hue API
print("\nPhilips Hue API connection status:")
try:
    api.load_existing()
except BaseException:
    api.create_new_user(bridge_address)
    api.print_debug_info()
    api.save_api_key()
    print("")
finally:
    # this should be in a try too
    api.fetch_lights()
    print(colored("[OK]", "green"), "Detected", len(api.fetch_lights()), "lights")
    api.list_lights()

# monitor connection status
BLE_HUE_class = BLE_HUE(address=transmitter_address, timeout=connection_timeout)
print("\nBluetooth connection status:")
while True:
    try:
        BLE_HUE_class.ble_detection()
    except KeyboardInterrupt:
        print("\n\nSession connection statistics:", end = "\n")
        print(colored("Connected", "green"), connection_statistics["connected"],
        colored("RSSI limit hit", "yellow"), connection_statistics["rssi_limit"],
        colored("Disconnected", "red"), connection_statistics["disconnected"])
        print(colored("\nEnd of session.", "dark_grey"))
        raise SystemExit