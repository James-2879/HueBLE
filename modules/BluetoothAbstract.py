import asyncio
from bleak import BleakScanner # https://bleak.readthedocs.io/en/latest/api/scanner.html

class BluetoothAbstract:        
    def __init__(self, address, timeout):
        """
        Backend stuff for BLE device discovery.
        
        This shouldn't need to be changed.
        """
        self.address = address
        self.timeout = timeout
    
    async def _discover(self):
        """Discover transmitter and RSSI."""
        result = await BleakScanner.find_device_by_address(self.address, self.timeout)
        return(result)
    
    def _async_discover(self):
        """Create and set event loop."""
        loop = asyncio.new_event_loop() # create loop for BLE detection
        asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self._discover())
        return(result)
    
    @property
    def rssi(self):
        """Return RSSI if possible."""
        connection = self._async_discover()
        try:
            return(connection.rssi)
        except AttributeError:
            return(None)
