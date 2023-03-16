## Pseudocode
```
async def gatherer():
    # We create a list named tasks
    for each service in the sockets.json file, we run what's below:
        Create a Heartbeat class and pass the information contained in the service
        Append to the tasks list a create_task function containing the start() function of the Heartbeat class
        
    We asyncio.gather(*tasks) to run multiple coroutines concurrently

async def main():
    Create task for gatherer function
    Await the above task

Run main function
```

## Setup new socket
```json
[
    {
        "Name":"Name of service",
        "URL":"ws://IP:PORT/",
        "Webhook":"Discord Webhook. e.g: https://discord.com/api/webhooks/...",
        "Message":"Personalized Send Message",
        "Interval": "How often to ping the socket. Has to be a number",
        "Timeout": "webhook.send timeout. Has to be a number"
    },
    {
        "Name":"Example",
        "URL":"ws://localhost:8000/",
        "Webhook":"Discord Webhook. e.g: https://discord.com/api/webhooks/...",
        "Message":"Personalized Send Message",
        "Interval":5,
        "Timeout":5
    }
]
```
