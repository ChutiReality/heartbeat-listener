import json
import time
import asyncio
import threading

from modules import utils
from modules import heartbeat

with open("sockets.json", "r", encoding="utf8") as _sockets:
    sockets = json.load(_sockets)

async def gatherer():
    tasks = []
    for service in sockets:
        hb_class = heartbeat.Heartbeat(
            name = service["Name"], 
            send_message = service["Message"], 
            interval = service["Interval"], 
            timeout = service["Timeout"]
        )
        tasks.append(asyncio.create_task(hb_class.start()))
        
    await asyncio.gather(*tasks)

async def main():
    gatherer_task = asyncio.create_task(gatherer())
    await gatherer_task

asyncio.run(main())
