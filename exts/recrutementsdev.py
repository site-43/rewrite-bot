import interactions
from utils.embeds import create_error_embed
class Extension(interactions.Client):
    def __init__(self, client):
        self.client : interactions.Client = client

    @interactions.extension_command(
        name="recrutementsdev",
        description="Commence les recrutements dev.",
        #scope=[655335475057393679, 675379685869486080],
        options=[
            interactions.Option(
                type=interactions.OptionType.USER,
                name="membre",
                description="Le membre dont vous vous souhaitez créer un salon recrutement dev.",
                required=True
            )
        ]
    )
    async def recrutementsdev(self, ctx: interactions.CommandContext, membre: interactions.User):
        if not ctx.author.id in []:
            await ctx.send(embeds=[create_error_embed("Vous n'avez pas la permission d'utiliser cette commande, vous n'êtes pas dans la Gestion développement.")])
            return

def setup(client):
    Extension(client)