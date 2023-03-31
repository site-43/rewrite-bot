import interactions
from utils.RobloxApiBridge import get, GetUserIdFromName
from utils.embeds import create_error_embed, new_embed
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
            currentUser = await GetUserIdFromName(pseudo=pseudonyme)
        else:
            currentUser = userid
        
        data = await get(url=f'/standard-datastores/datastore/entries/entry?datastoreName=V2&entryKey=heheboi_{currentUser}', headers={})
        if data == False:
            await ctx.send(embeds=[create_error_embed("Aucune entrée n'a été trouvée avec cet utilisateur.")])
            return
        json = await data.json()
        isReported = "Non" if json["Data"]["Reported"] == False else "Oui"
        await ctx.send(embeds=[
            new_embed(
                title="Statistiques du joueur",
                description="Consultez les informations de l'individu.",
                fields=[
                    ["XP", json["Data"]["Experience"], False],
                    ["Dernière update des données", f'<t:{json["MetaData"]["LastUpdate"]}:R>', False],
                    ["Report actif", isReported, False]
                ]
            )
        ])


def setup(client):
    Extension(client)