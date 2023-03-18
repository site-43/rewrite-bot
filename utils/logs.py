import interactions
async def new_log(
  client = None,
  text:str = None,
  channel: int = 1080204593016881153,
  embeds:dict = []
) -> interactions.Channel:
  if client == None:
    print("Erreur, le client n'est pas bien configuré.")
  channel = await interactions.get(client, interactions.Channel, object_id=channel)
  message = await channel.send(content=text, embeds=[embed for embed in embeds])
  return message


def setup(client):
  Logger(client=client)