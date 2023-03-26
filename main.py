import interactions
from interactions.ext import molter
from flask import Flask
from hypercorn.config import Config
from hypercorn.asyncio import serve
from asgiref.wsgi import WsgiToAsgi
import asyncio
import logging
import datetime
import time
import os
from configs import VERSION, OWNER_ID
from dotenv import load_dotenv

load_dotenv()
EXTENSIONS = [file.replace(".py", "") for file in os.listdir("exts") if file.endswith(".py")]

# client = interactions.Client(token="") -> Bot Canarypy 
client = interactions.Client(
    token=os.getenv("TOKEN"),
    intents=interactions.Intents.DEFAULT
    | interactions.Intents.GUILD_MESSAGE_CONTENT
    | interactions.Intents.GUILD_MEMBERS,
    disable_sync=False,
    #logging=True,
)
# app = Flask(__name__)
# config = Config()
# config.bind = ["0.0.0.0:80"]

molter.setup(client, default_prefix=["s!","<"])
[client.load(f"exts.{EXT}") for EXT in EXTENSIONS]


# @app.route('/')
# async def home():
#      return 'Running !'
# loop = asyncio.get_event_loop()

# task1 = loop.create_task((serve(WsgiToAsgi(app), config)))
# task2 = loop.create_task(client._ready())

# gathered = asyncio.gather(task1,task2)
# loop.run_until_complete(gathered)
print("Je viens d'être démarré !")
client.start()