import aiohttp
baseURL = "https://apis.roblox.com/datastores/v1/universes/1578560485"
basicheaders = {}
async def get(
    url:str,
    datastore_name:str = "V2",
    datastore_entrykey:str = None,
    headers:dict = None
):
    if not url:
        return False
    response = aiohttp.request("GET", baseURL+url, headers={})