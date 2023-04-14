import interactions
from utils.embeds import new_embed, new_notify_embed, create_error_embed

class Extension(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client
    
    @interactions.extension_command(
        name="embed",
        description="Crée un embed et l'envoie dans le salon demandé à travers un Webhook.",
        options=[
            interactions.Option(name="webhookname", description="Nom du Webhook", required=True, type=interactions.OptionType.STRING),
            interactions.Option(name="titre", description="Titre de l'embed", required=True, type=interactions.OptionType.STRING),
            interactions.Option(name="description", description="Description de l'embed", required=False, type=interactions.OptionType.STRING),
            #interactions.Option(name="couleur", description="Couleur sous la forme Hexadécimale sous forme 0x######", required=False, type=interactions.OptionType.STRING)
        ]
    )
    async def embed(self, ctx: interactions.CommandContext, webhookname:str, titre: str, description: str = None, couleur: str = None):
        await ctx.send(embeds=[new_notify_embed("<a:loading:1086257424534605975> Génération de l'embed en cours.")], ephemeral=True)
        webhook = await interactions.Webhook.create(client=self.client._http, channel_id=int(ctx.channel_id), name=webhookname)
        await webhook.execute(embeds=[new_embed(title=titre, description=description, color=couleur)])
        await webhook.delete()
        

def setup(client):
    Extension(client)