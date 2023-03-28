import aiohttp
from os import getenv
from dotenv import load_dotenv
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
        print(await response.json())
        return response
