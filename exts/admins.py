import interactions
from utils.embeds import new_embed
from utils.components import modals
import datetime
import asyncio
class Extension(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client

    @interactions.extension_modal("admin_propose")
    async def admin_propose(self, ctx: interactions.ComponentContext, propositionName:str, propositionDescription:str):
        await ctx.defer(True)
        channel = await interactions.get(self.client, interactions.Channel, object_id=1096559829184696402)
        channelAdmin = await interactions.get(self.client, interactions.Channel, object_id=1055044493700780042)
        message = await channel.send(embeds=[new_embed(title=propositionName, description=propositionDescription, footer_text=f"Proposition de sujet par {ctx.author.name or ctx.author.user.username}")])
        await channelAdmin.send(embeds=[message.embeds[0]])
        await asyncio.sleep(1)
        await message.create_reaction(emoji="👍")
        await message.create_reaction(emoji="👎")
        await asyncio.sleep(1)
        await ctx.send("Votre proposition a bien été reçue !\nVous pouvez la consulter dès maintenant.", ephemeral=True)


    # @interactions.extension_command(name="setup_propos", description="Qu'est-ce que tu regardes. . .")
    # async def setuppropose(self, ctx: interactions.CommandContext):
    #     channel = await interactions.get(self.client, interactions.Channel, object_id=1096559829184696402)
    #     if channel:
    #         await channel.send(
    #             embeds=[new_embed(title="Transmettre un sujet de réunion", description="Proposez vos sujets à l'Administration du Site-43 via le bouton ci-dessous.", fields=[["Temps d'ouverture", "Samedi 00:00 -> Jeudi 23:59", False]], footer_text="Système de propositions Admin.")],
    #             components=[interactions.Button(style=interactions.ButtonStyle.SECONDARY, label="Proposer un sujet", custom_id="propose_admin")]
    #             )
            
    
    @interactions.extension_component("propose_admin")
    async def propose(self, ctx: interactions.ComponentContext):
        now = datetime.datetime.now()
        if now.weekday() in range(4,5):
            await ctx.send(embeds=[new_embed(title="Erreur", description="Cette commande n'est pas disponible actuellement. Veuillez consulter les heures d'ouverture.", color=0x8F0505)], ephemeral=True)
            return
        else:
            await ctx.popup(modal=modals["Proposition Admin"])

def setup(client: interactions.Client):
    Extension(client)