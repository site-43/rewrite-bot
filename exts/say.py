import interactions
from utils.components import modals
from utils.embeds import new_notify_embed
class Extension(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client

    @interactions.extension_modal("say_msg")
    async def say_msg(self, ctx: interactions.ComponentContext, salonid:int = None, text: str = None):
        if text == None:
            return
        if salonid:
            try:
                channel = interactions.get(self.client, interactions.Channel, object_id=int(salonid))
            except:
                await ctx.send('Le salon est invalide', ephemeral=True)
                return
        else:
            channel = ctx.channel
        message = await channel.send(text)
        await ctx.send(embeds=[new_notify_embed(f"Votre [message](https://discord.com/channels/{int(ctx.guild_id)}/{int(ctx.channel_id)}/{int(message.id)}) a été envoyé.")], ephemeral=True)

    @interactions.extension_command(name="say",description="Utiliser le bot pour parler à sa place.")
    async def say(self, ctx:interactions.CommandContext):
        await ctx.popup(modal=modals["SayMessage"])


def setup(client: interactions.Client):
    Extension(client)