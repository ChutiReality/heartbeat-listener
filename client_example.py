import asyncio
import websockets

async def websocket_server(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send(message)

async def start_server():
    async with websockets.serve(websocket_server, "localhost", 8000) as server:
        print(server)
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(start_server())