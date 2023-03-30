import aiohttp
from os import getenv
from dotenv import load_dotenv
import json
load_dotenv()
baseURL = "https://apis.roblox.com/datastores/v1/universes/1578560485"
basicheaders = {"x-api-key": getenv("ROBLOX_API_KEY")}
async def get(
    url:str = None,
    datastore_name:str = "V2",
    datastore_entrykey:str = None,
    headers:dict = None
):
    if not url:
        return False
    for header in basicheaders.keys():
        headers[header] = basicheaders[header]
    async with aiohttp.request("GET", baseURL+url, headers=headers) as response:
        json = await response.json()
        if 'error' in json:
            return False
        else:
            return response

async def GetUserIdFromName(pseudo:str = None):
    if not pseudo:
        return False
    
    data = {"usernames": [pseudo], "excludeBannedUsers": True}
    jdata = json.dumps(data)
    async with aiohttp.request("POST", "https://users.roblox.com/v1/usernames/users", data=jdata) as response:
        respJSON = await response.json()
        if len(respJSON['data']) == 1:
            return respJSON['data'][0]['id']
        elif len(respJSON['data']) > 1:
            return "TooMuch"
        else:
            return False