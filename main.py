from modules import utils
import asyncio
import json

from modules import heartbeat

with open("sockets.json", "r", encoding="utf8") as _sockets:
    sockets = json.load(_sockets)

for service in sockets:

    hb = heartbeat.Heartbeat(
        name = service["Name"],
        send_message = service["Message"],
        interval = service["Interval"],
        timeout = service["Timeout"]
    )

asyncio.run(hb.start())