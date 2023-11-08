from modules.BluetoothLogicClient import *
from modules.BluetoothLogic import *
from modules.Activities import *
from modules.Utilities import *
from termcolor import colored

class BluetoothRunner:        
    def __init__(self, address, timeout, rssi_mode, rssi_limit, activities, client):
        self.bluetooth = BluetoothLogic(address = address, timeout = timeout, rssi_mode = rssi_mode, rssi_limit = rssi_limit, client = client)
        self.activities = activities
        self.transmitter_status = None
        self.connection_attempts = 0
        self.connection_statistics = dict(connected = 0, disconnected = 0, rssi_limit = 0)
        self.activity_paused = False
        
    def runner(self):
        """Define how to handle transmitter out of range."""
        state = self.bluetooth.state
        rssi = self.bluetooth.rssi
        if state == "connected":
            self.connection_attempts = 0 # reset
            self._output(state, rssi)
            if self.activity_paused is True: # pause any actions until connection drop and restore
                self.activities.on_connect()
                self.activity_paused = False # block re-execution
        elif state == "rssi_limit" or state == "disconnected":
            self.connection_attempts += 1
            self._output(state)
            if self.connection_attempts == 3:
                self.activities.on_drop()
                self.activity_paused = True      
        
    def _output(self, state, rssi = None):
        self.connection_statistics[state] += 1
        Utilities.clear_terminal("recursive")
        if state == "connected":
            print(colored("[OK]", "green"), colored("Detected", "green"),  "RSSI:", rssi, end = "\r") 
        elif state == "rssi_limit":
            print(colored("[!!]", "red"), self.connection_attempts, "failed connection attempts", colored("RSSI limit", "yellow"), end = "\r")
        elif state == "disconnected":
            print(colored("[!!]", "red"), self.connection_attempts, "failed connection attempts", colored("Disconnected", "red"), end = "\r")
            
    def end(self):
        print("\n\nSession connection statistics:", end = "\n")
        print(colored("Connected", "green"), self.connection_statistics["connected"],
        colored("RSSI limit hit", "yellow"), self.connection_statistics["rssi_limit"],
        colored("Disconnected", "red"), self.connection_statistics["disconnected"])
        print(colored("\nEnd of session.", "dark_grey"))
        input(colored("\nPress 'Enter' to exit.", "dark_grey"))
        raise SystemExit