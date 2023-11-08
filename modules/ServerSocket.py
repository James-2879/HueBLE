import asyncio
from websockets.server import serve

class ServerSocket:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.rssi = None
    
    async def echo(self, websocket):
        async for message in websocket:
            await websocket.send(message)
            self.rssi = message

    async def main(self):
        async with serve(self.echo, self.ip_address, int(self.port)): # str int issues ?
            await asyncio.Future()  # run forever


# asyncio.run(main())