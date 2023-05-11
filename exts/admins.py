import interactions
from utils.embeds import new_embed
from utils.components import modals
import datetime
class Extension(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client

    @interactions.extension_modal("admin_propose")
    async def admin_propose(self, ctx: interactions.ComponentContext, propositionName:str, propositionDescription:str):
        channel = await interactions.get(self.client, interactions.Channel, object_id=1096559829184696402)
        channelAdmin = await interactions.get(self.client, interactions.Channel, object_id=1055044493700780042)
        message = await channel.send(embeds=[new_embed(title=propositionName, description=propositionDescription, footer_text=f"Proposition de sujet par {ctx.author.name or ctx.author.user.username}")])
        await message.create_reaction(emoji="👍")
        await message.create_reaction(emoji="👎")
        await channelAdmin.send(embeds=[message.embeds[0]])
        await ctx.send("Votre proposition a bien été reçue !\nVous pouvez la consulter dès maintenant.", ephemeral=True)


    @interactions.extension_command(name="setup_propos", description="Qu'est-ce que tu regardes. . .")
    async def setuppropose(self, ctx: interactions.CommandContext):
        channel = await interactions.get(self.client, interactions.Channel, object_id=1096559829184696402)
        if channel:
            await channel.send(
                embeds=[new_embed(title="Transmettre un sujet de réunion", description="Proposez vos sujets à l'Administration du Site-43 via le bouton ci-dessous.", fields=[["Temps d'ouverture", "Samedi 00:00 -> Jeudi 23:59", False]], footer_text="Système de propositions Admin.")],
                components=[interactions.Button(style=interactions.ButtonStyle.SECONDARY, label="Proposer un sujet", custom_id="propose_admin")]
                )
            
    
    @interactions.extension_component("propose_admin")
    async def propose(self, ctx: interactions.ComponentContext):
        await ctx.popup(modal=modals["Proposition Admin"])

def setup(client: interactions.Client):
    Extension(client)