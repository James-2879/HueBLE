from websockets.sync.client import connect

class ClientSocket:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        
    def send_rssi(self, rssi):
        with connect("ws://"+self.ip_address+":"+self.port) as websocket:
            websocket.send(str(rssi))
            message = websocket.recv()
            # print(f"Received: {message}") # for debugging mostly