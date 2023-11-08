import os
import time
from termcolor import colored
from hue_api import HueApi # http://hue-py-docs.s3-website-us-east-1.amazonaws.com/index.html

from modules.Utilities import *

class PhilipsHue:
    def __init__(self, bridge, lights):
        """
        Setup Hue API connection before BLE detection methods are run.
        
        Further methods may be added below to control Hue, and called from Activities.
        """
        if bridge is None:
            print("Edit the 'User Config' section of hue_beacon.py with the bridge address.")
            raise SystemExit
        self.bridge = bridge
        self.lights = lights
        self.api = HueApi()   
        self._setup()
        
    def _setup(self):
        """Load existing Hue config or create new one."""
        try:
            self.api.load_existing() # attempt to load existing config
        except BaseException:
            result = None
            tries = 0
            print("\nPress pairing button on Hue bridge.\n")
            while tries < 10 and result is None: # give up after this number
                try:
                    self.api.create_new_user(self.bridge)
                    Utilities.clear_terminal("recursive")
                    self.api.print_debug_info()
                    try:
                        self.api.save_api_key()
                        print("\nCached API key locally.")
                    except FileNotFoundError as error:
                        print("\nUnable to cache API key!")
                        print(error)
                    finally:
                        result = True
                except Exception:
                    tries += 1
                    print("[Attempt "+str(tries)+"/20] Searching for Hue bridge...", end = "\r")
                    time.sleep(3)
            Utilities.clear_terminal("new")
            if tries == 10:
                print("\nUnable to connect to Hue bridge.")
                for x in range(5):
                    time.sleep(1)
                    print("Exiting program in "+str(x)+"s", end = "\r") 
                raise SystemExit
        try:
            self.api.fetch_lights()
            print("\nPhilips Hue API connection status:")
            print(colored("[OK]", "green"), "Detected", len(self.api.fetch_lights()), "lights")
            self.api.list_lights()
        except AttributeError as error:
            print(error)
            os.system('pause')
            raise SystemExit
        
    def hue_on(self):
        self.api.turn_on(self.lights)
        
    def hue_off(self):
        self.api.turn_off(self.lights)