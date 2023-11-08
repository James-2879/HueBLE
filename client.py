build_number = 16032023

#-------------------------------- User Config ---------------------------------

# transmitter_address = "ED:7E:B6:76:9C:0C"
# transmitter_address = "A0:38:F8:4C:24:97" # Oura
# transmitter_address = "04:72:95:24:36:16"
transmitter_address = "DB:90:14:18:18:20" # JUUL
connection_timeout = 3 #seconds

#------------------------------------------------------------------------------
#--------------------------------- Packages -----------------------------------

from modules.BluetoothAbstract import *
from modules.ClientSocket import *
from modules.Utilities import *

#---------------------------------- Preamble ------------------------------------

if transmitter_address is None:
    print("Edit the 'User Config' section of hue_beacon.py with the transmitter address.")
    raise SystemExit

print("\n> Build prototype #"+str(build_number))
print("\nDeveloped by James Swift 2023")
print("Latest versions and documentation available at https://github.com/James-2879/<repo-name>")

#---------------------------------- Script ------------------------------------

bluetooth = BluetoothAbstract(address = transmitter_address,
                            timeout = connection_timeout)
socket = ClientSocket(ip_address = "192.168.0.25",
                      port = "8765")

print("\nBluetooth connection status:")
while True:
    try:
        rssi = bluetooth.rssi
        Utilities.clear_terminal("recursive")
        print("RSSI:", rssi, end = "\r")
        socket.send_rssi(rssi)
    except KeyboardInterrupt:
        print("Exiting...")
        raise SystemExit


