from interactions import *
from interactions.ext.molter import setup, MolterCommand, prefixed_command, MolterContext

class Ext(Extension):
    def __init__(self, client):
        self.client:Client = client
        setup(client=self.client, default_prefix=".s")

    @prefixed_command(name="setpresence")
    async def presence(self, ctx: MolterContext, *, message):
        presence =  ClientPresence(
            activities=[
                PresenceActivity(
                    name=message,
                    type=PresenceActivityType.GAME
                )
            ]
        )
        self.client.change_presence(presence)
        await ctx.send("Modifications faites.")