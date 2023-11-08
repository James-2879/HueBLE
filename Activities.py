from modules.Utilities import *
from modules.PhilipsHue import *

class Activities:
    def __init__(self, bridge, lights):
        """
        Define actions based on connection state.
        
        New actions should be added as a static method to Utilities.
        """
        self.hue = PhilipsHue(bridge = bridge, lights = lights)
    
    def on_drop(self):
        """Do this when connection is lost."""
        Utilities.lock_workstation()
        self.hue.hue_off()
    
    def on_connect(self):
        """Do this when connection is restored."""
        Utilities.wake_workstation()
        self.hue.hue_on()