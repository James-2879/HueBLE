import time

class BluetoothLogicClient:
    def __init__(self, rssi_mode, rssi_limit, rssi):
        """
        Return values for use with BluetoothRunner.
        
        Serves as a mid-level abstraction between BluetoothRunner and BluetoothAbstract.
        """
        self.rssi_mode = rssi_mode
        self.rssi_limit = rssi_limit
        self.rssi = rssi

    def _determine_state(self):
        """Define actions base on connection state."""
        rssi = self.rssi
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