import interactions

async def new_log(
  self = interactions.Extension.client,
  text:str = None,
  channel: int = 1080204593016881153,
) -> interactions.Channel:
    channel = await interactions.get(self, interactions.Channel, object_id=channel)
    message = await channel.send(content=text)
    return message