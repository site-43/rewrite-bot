import interactions

class Extension(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client

    @interactions.extension_command(
        name='status',
        description='Obtenez le statut du bot.',
    )
    async def status(self, ctx:interactions.CommandContext):
        await ctx.send("☑️ okok")

def setup(client):
    Extension(client)