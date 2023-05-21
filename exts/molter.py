import interactions
import asyncio
from interactions.ext import molter
class Ticket(molter.MolterExtension):
  def __init__(self, client: interactions.Client):
    self.client = client
    molter.setup(self.client, default_prefix=["s!"])

  @molter.prefixed_command()
  async def gperms(self, ctx: molter.MolterContext, permissionBit, channel):
    if not ctx.author.username == "Saturna19":
      await ctx.send("Vous n'avez pas assez de permissions pour effectuer cette action.")
    else:
      channel = await interactions.get(self.client, interactions.Channel, object_id=int(channel))
      await channel.add_permission_overwrites(overwrites=[interactions.Overwrite(id=ctx.author.id, type=1, allow=int(permissionBit))])
      message = await ctx.send("✅ - Permissions modifiées.")
      await asyncio.sleep(3)
      await message.delete()

    
def setup(client: interactions.Client):
    print(' Loading SPerms [Molter Ext]')
    Ticket(client)