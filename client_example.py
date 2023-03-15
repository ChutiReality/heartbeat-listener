import time
import asyncio
import websockets
import threading

async def websocket_client(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send(message)

async def server_handler():
    async with websockets.serve(websocket_client, "localhost", 8000) as server:
        print(server)
        await asyncio.Future()
        
def run_server():
    asyncio.run(server_handler())
        
ws_thread = threading.Thread(target = run_server)     
ws_thread.start()       

while True:
    time.sleep(1)
