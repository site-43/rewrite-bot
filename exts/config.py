import interactions
import asyncio
from utils.embeds import new_embed, new_notify_embed
class configurator(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="config",
        description="Configure le bot.", 
        options=[
            interactions.Option(name="new", description="Ajoute des options de configuration.", type=interactions.OptionType.SUB_COMMAND, options=[
                interactions.Option(name="gerants", description="Rôle des gérants du serveur.", required=True, type=interactions.OptionType.ROLE),
                interactions.Option(name="gannouncement", description="Salon dans lequel envoyer les actualités aux gérants.", required=True, type=interactions.OptionType.CHANNEL),
                interactions.Option(name="announcement", description="Salon dans lequel envoyer les actualités au personnel.", required=True, type=interactions.OptionType.CHANNEL),
            ]),
            interactions.Option(name="reset", description="Retire toutes les options de configuration.", type=interactions.OptionType.SUB_COMMAND)
        ]
    )
    async def config(self, ctx:interactions.CommandContext, sub_command:str, gerants:interactions.Role = None, gannouncement:interactions.Channel = None, announcement:interactions.Channel = None):
        if sub_command == "new":
            currentMessage = await ctx.send(embeds=[new_notify_embed("<a:loading:1086257424534605975> Début de la procédure de configuration...")])
            await asyncio.sleep(2)
            await currentMessage.edit(embeds=[new_embed(
                title="Configuration",
                description="La configuration est en cours de progression, voici les informations qui sont enregistrées:",
                fields=[["Rôle des gérants", gerants.mention, False], ["Salon des annonces gérants", gannouncement.mention, False], ["Salon des annonces personnel", announcement.mention, False]],
                footer_text=f"Configuration par {ctx.author.name}"
            )])

def setup(client):
    configurator(client)