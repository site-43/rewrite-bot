import interactions
import platform
import psutil
class Extension(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="status",
        description="Obtenir le statut du bot",
    )
    async def status(self, ctx:interactions.CommandContext):
        print(psutil.disk_usage("/"))

def setup(client: interactions.Client):
    Extension(client)
    