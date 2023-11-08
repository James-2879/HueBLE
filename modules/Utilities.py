import ctypes
import platform
import mouse

class Utilities:
    def __init__(self):
        """
        Possible utilities that can be called in response to change in connection state or other.
        
        These utilities should be included in Activities methods if they are required.
        """
        pass
    
    @staticmethod
    def lock_workstation():
        if platform.system() == "Windows":
            ctypes.windll.user32.LockWorkStation()
                
    @staticmethod
    def wake_workstation():
        # keyboard.press_and_release('ctrl')
        mouse.move(0, 10, absolute=False, duration=0.25)
        mouse.move(10, 0, absolute=False, duration=0.25)
        mouse.move(0, -10, absolute=False, duration=0.25)
        mouse.move(-10, 0, absolute=False, duration=0.25)
    
    @staticmethod        
    def clear_terminal(end):
        if end == "recursive":
            print("                                                                        ", end = "\r")
        if end == "new":
            print("                                                                        ", end = "\n")