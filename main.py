import interactions
from interactions.ext import molter
from flask import Flask
from hypercorn.config import Config
from hypercorn.asyncio import serve
from asgiref.wsgi import WsgiToAsgi
import asyncio
from colorama import Fore, Style
import logging
import datetime
import time
import os
from dotenv import load_dotenv

load_dotenv()
EXTENSIONS = [file.replace(".py", "") for file in os.listdir("exts") if file.endswith(".py")]
Loaded_Exts = []

client = interactions.Client(
    token=os.getenv("TOKEN"),
    intents=interactions.Intents.DEFAULT
    | interactions.Intents.GUILD_MESSAGE_CONTENT
    | interactions.Intents.GUILD_MEMBERS,
    disable_sync=False,
    default_scope=[ 675379685869486080, 1023676017493147648] #675379685869486080,
    #logging=True,
)
# app = Flask(__name__)
# config = Config()
# config.bind = ["0.0.0.0:80"]

# molter.setup(client, default_prefix=["s!","<"])
# [client.load(f"exts.{EXT}") for EXT in EXTENSIONS]
for ext in EXTENSIONS:
    try:
        client.load(f"exts.{ext}")
        print(f"Loaded {ext}")
        Loaded_Exts.append(ext)
    except:
        print(f"{Fore.RED}[ERROR]{Fore.RESET} {Fore.LIGHTYELLOW_EX}Failed{Fore.RESET} to load extension {ext}")


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