import time

from modules.BluetoothAbstract import *

class BluetoothLogic:
    def __init__(self, address, timeout, rssi_mode, rssi_limit, client):
        """
        Return values for use with BluetoothRunner.
        
        Serves as a mid-level abstraction between BluetoothRunner and BluetoothAbstract.
        """
        self.bluetooth = BluetoothAbstract(address = address, timeout = timeout)
        self.timeout = timeout
        self.rssi_mode = rssi_mode
        self.rssi_limit = rssi_limit
        self.client = client

    def _determine_state(self):
        """Define actions base on connection state."""
        if self.client is None:
            rssi = self.bluetooth.rssi
            if rssi is not None:
                if self.rssi_mode is True:
                    if rssi < self.rssi_limit: # connected but out of range
                        time.sleep(self.timeout) # this is okay for now
                        return("rssi_limit")
                    elif rssi >= self.rssi_limit: # connected and in range
                        return("connected")
                if self.rssi_mode is False: # connected
                    return("connected")
            if rssi is None: # not connected
                return("disconnected")
        if self.client is not None:
            rssi = self.bluetooth.rssi
            client_rssi = self.client.rssi
            # sort out this logic and hopefully everything works.
            
            
    @property
    def state(self):
        """Return a string describing the connection state."""
        state = self._determine_state()
        return(state)
    
    @property
    def rssi(self):
        """Return the RSSI (as an integer) if possible, else None."""
        rssi = self.bluetooth.rssi
        return(rssi)