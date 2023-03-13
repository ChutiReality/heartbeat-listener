import json
import time
import asyncio
import traceback
import websockets

from pathlib import Path
from modules.utils import Utils

root_path = str(Path(__file__).parent.parent)

class Heartbeat(Utils):
    def __init__(self, name, send_message, interval, timeout):
      super().__init__()
      """
      Args: 
        name         : str : main key name in sockets.json
        send_message : str : message to send to url
        interval     : int : wait time before recv'ing again
        timeout      : int : recv timeout
      """
      self.name = name
      socket = self.get_sockets()
      self.url = socket["URL"] # Websocket URL
      self.webhook_url = socket["Webhook"]
      self.send_message = send_message # Message to send
      self.interval = interval # Interval per ping
      self.timeout = timeout # Recv timeout
 
      self.is_running = False
      self.alerted_shutdown = False

    def get_sockets(self):
        with open(root_path + "/sockets.json", "r", encoding = "utf8") as sockets:
            data = json.load(sockets)
            for item in data:
                if item["Name"] == self.name:
                    return item

    async def check_heartbeat(self):
        try:
            async with websockets.connect(self.url) as websocket:
                # Send message to the websocket
                await websocket.send(self.send_message) 

                # Wait for a response
                response = await asyncio.wait_for(websocket.recv(), timeout = self.timeout)
                print(response)
                # Store response and get the   
                self.last_response = response
                # If this is true, it means its back up after being down
                if self.alerted_shutdown == True:
                    # Tell the script is online again
                    self.log("info", f"{self.name} is online again.")
                    self.out_log("info", f"{self.name} is online again.")
                    self.alerted_shutdown = False
        except Exception as error:
            if error.args[3] == 1225:
                # Socket isnt alive
                # If we didnt inform about it, infom
                if self.alerted_shutdown == False:   
                    self.log("warning", f"{self.name} stopped answering ({error.args[3]})")
                    self.out_log("warning", f"{self.name} stopped answering ({error.args[3]})")
                    self.alerted_shutdown = True

    async def start(self):
        self.is_running = True
        while self.is_running:
            await self.check_heartbeat()
            await asyncio.sleep(self.interval)
            
    async def stop(self):
        self.is_running = False