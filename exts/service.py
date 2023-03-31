import interactions
from utils.embeds import new_embed, new_notify_embed, create_error_embed
import time
from utils.database import getData, addData, getCount, deleteData
from utils.components import add_button
class Extension(interactions.Extension):
    def __init__(self, client):
        self.client : interactions.Client = client

    @interactions.extension_component("TakeService")
    async def TakeService(self, ctx: interactions.ComponentContext):
        data = await getData(collection="services", searchValue = {"_id":int(ctx.author.id)})
        if data == None:
            await addData(collection="services", document={"_id": int(ctx.author.id), "startTime": int(time.time())})
            await ctx.send(embeds=[new_notify_embed("Bienvenue en service !")], ephemeral=True)
        else:
            await ctx.send(embeds=[create_error_embed(f"Vous avez déjà un service en cours. Vous l'avez lancé à <t:{data['startTime']}:t>")], ephemeral=True)
    
    @interactions.extension_component("StopService")
    async def StopService(self, ctx: interactions.ComponentContext):
        data = await getData(collection="services", searchValue = {"_id":int(ctx.author.id)})
        if data == None:
            await ctx.send(embeds=[create_error_embed("Vous n'êtes pas en service.")], ephemeral=True)
        else:
            await deleteData(collection="services", searchValue={"_id": int(ctx.author.id)})

    @interactions.extension_command(
        name="sendservice",
    )
    async def sendservice(self, ctx: interactions.CommandContext):
        await ctx.send(
            embeds=[
                new_embed(
                    title="Service",
                    description="Prenez/arrêtez votre service avec le bouton çi-dessous.\nIl permets de vous octroyer le rôle En jeu, ainsi que de compter votre temps.",
                    color=0xb39317,
                    fields=[["Modérateurs en jeu", await getCount(collection="services"), False]]
                )
            ],
            components=[
                add_button(label="Prise de service", custom_id="TakeService"),
                add_button(style=interactions.ButtonStyle.DANGER, label="Fin de service", custom_id="StopService")
            ]
        )

def setup(client):
    Extension(client)