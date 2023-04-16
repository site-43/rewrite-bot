import interactions
import platform
import psutil
import utils.embeds
import time
start_time = time.time()
class Extension(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="status",
        description="Obtenir le statut du bot",
    )
    async def stats(self, ctx:interactions.CommandContext):
        print(psutil.disk_usage("/"))
        print(platform.system)
        owner: interactions.User = interactions.get(self.client, interactions.User, object_id=self.client.me.team.owner_user_id)
        embed = utils.embeds.new_embed(
            title="Statut du bot",
            color=0xfcc38d,
            description=f"Voici le statut du bot {self.client.me.name} !",
            thumb=self.client.me.icon_url,
            fields=[
                ["Système d'exploitation", "<:Windows:1097148342410170448> Windows" if platform.system() == "Windows" else "Undefined", True],
                ["Version du serveur", platform.version(), True],
                ["Serveurs", f"{len(self.client.guilds)} serveurs", True],
                ["Démarrage du serveur", f"<t:{start_time:.0f}:R>", True],
                ["Développeur", f"{owner.mention}", True],
                ["Commandes", len(self.client._commands), True]
            ]
        )
        await ctx.send(embeds=[embed])

def setup(client: interactions.Client):
    Extension(client)
    