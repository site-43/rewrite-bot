import interactions
from utils.RobloxApiBridge import get, GetUserIdFromName
from utils.embeds import create_error_embed
class Extension(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client

    @interactions.extension_command(
        name='rprofiles',
        description='Obtenez le profil d\'un utilisateur avec son pseudo/userid.',
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="pseudonyme",
                description="Pseudonyme (Lettres à la casse.)",
                required=False,
            ),
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="userid",
                description="UserID ROBLOX de l'utilisateur",
                required=False,
            )
        ]
    )
    async def status(self, ctx:interactions.CommandContext, pseudonyme:str = None, userid:str = None):
        await ctx.defer(ephemeral=True)
        if not pseudonyme and not userid:
            await ctx.send(embeds=[create_error_embed("Veuillez entrer un pseudonyme ou identifiant de compte.")], ephemeral=True)
            return False
        currentUser = None
        if pseudonyme:
            currentUser = await GetUserIdFromName()
        else:
            currentUser = userid
        
        data = await get(url=f'/standard-datastores/datastore/entries/entry?datastoreName=V2&entryKey=heheboi_{currentUser}', headers={})
        json = await data.json()
        await ctx.send(content=f'XP: {json["Data"]["Experience"]}')


def setup(client):
    Extension(client)