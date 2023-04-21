import interactions
from interactions.ext.fastapi import setup
from colorama import Fore
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
api = setup(client, host="0.0.0.0",  port=8080)
for ext in EXTENSIONS:
    try:
        client.load(f"exts.{ext}")
        print(f"Loaded {ext}")
        Loaded_Exts.append(ext)
    except:
        print(f"{Fore.RED}[ERROR]{Fore.RESET} {Fore.LIGHTYELLOW_EX}Failed{Fore.RESET} to load extension {ext}")


@api.route("GET", "/")
async def index():
    return {"message": "success", "statut": "Alive"}

# @api.route("GET", "/services")
# async def services(optional: str = None):
#     return {"passed": optional if optional else "None."}

client.start()