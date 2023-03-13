import time
from pathlib import Path
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
import traceback
import json

root_path = str(Path(__file__).parent.parent)

with open(root_path + "/config.json", "r", encoding = "utf8") as _config:
    config = json.load(_config)

class Utils:
    def __init__(self):
        ...

    def out_log(self, level: str, message: str):
        """
        Send logs to other platforms
        
        Args:
            level   : str : info - warning - critical
            message : str : Message to describe the log  

        """
        try:
            emoji = ":warning:" if level == "warning" else ":information_source:" if level == "info" else ":red_circle:"
            
            webhook = DiscordWebhook(url = self.webhook_url)

            embed = DiscordEmbed(
                title = level.capitalize() + " " + f"{emoji}", 
                description = message
            )
            
            embed.set_footer(
                text = config["Discord"]["Webhook"]["Embed"]["Footer"], 
                icon_url = config["Discord"]["Webhook"]["Embed"]["Icon"]
            )
            embed.set_timestamp()
            webhook.add_embed(embed)

            response = webhook.execute()
            
        except Exception as error:
            print(traceback.format_exc())
            return traceback.format_exc()
                
        return "Done"

    def log(self, level: str, message: str):
        date = self.get_date()
        datetime = self.get_time()

        write_message = "{: <12} {: <10} {: <8} {: <10}".format(date, datetime, level.upper(), message)

        try:
            with open(root_path + f"/Logs/{self.name}.log", "a", encoding = "utf-8") as log_text_file:
                print(f"\nLog → {write_message}")
                log_text_file.write(write_message + "\n")

        except:
            print("Traceback caught")
            with open(root_path + "/Logs/service.log", "a", encoding = "utf-8") as log_text_file:
                write_message = "{: <12} {: <10} {: <8} {: <10}".format(date, datetime, "CRITICAL", f"\n{traceback.format_exc()}\n")
                log_text_file.write(write_message)
            
    def get_time(self) -> str:
        now_utc = datetime.utcnow()
        current_time = now_utc.strftime("%H:%M:%S") 
        return current_time

    def get_date(self) -> str:
        now_utc = datetime.utcnow()
        current_date = now_utc.strftime("%d/%m/%Y")
        return current_date
