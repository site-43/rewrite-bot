import interactions
from utils.components import modals
from utils.embeds import create_error_embed
class Extension(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client

    @interactions.extension_command(name="recruteur",description="Start recrutements dev.", scope=[655335475057393679], options=[interactions.Option(type=interactions.OptionType.USER, required=True, name="member", description="L'utilisateur")])
    async def recruteur(self, ctx:interactions.CommandContext, member: interactions.User):
        if not 1097936631501168732 in ctx.author.roles:
            await ctx.send(embeds=[create_error_embed("Vous n'êtes pas dans la gestion dev.")])
            return
        channel:interactions.Channel = await ctx.guild.create_channel(name=member.username, topic="Recrutement développeur.", type=interactions.ChannelType.GUILD_TEXT, permission_overwrites=[
            interactions.Overwrite(
                id=ctx.guild.id,
                type=0,
                allow=0,
                deny=1024,
            ),
            interactions.Overwrite(
                id=member.id,
                type=1,
                allow=3072,
                deny=0,
            ),
            interactions.Overwrite(
                id=1097936631501168732,
                type=0,
                allow=3088,
                deny=0
            )
        ], reason="Recrutements dev.", parent_id=1097920035781091328)
        await ctx.send(f"Le salon pour {member.mention} a été créé ({channel.mention})")
def setup(client: interactions.Client):
    Extension(client)