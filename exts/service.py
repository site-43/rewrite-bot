import interactions
from utils.embeds import new_embed, new_notify_embed, create_error_embed
import time
from utils.database import getData, addData, getCount, deleteData, updateData
from utils.components import add_button
compos = [
    add_button(label="Prise de service", custom_id="TakeService"),
    add_button(style=interactions.ButtonStyle.DANGER, label="Fin de service", custom_id="StopService")
]
class Extension(interactions.Extension):
    def __init__(self, client):
        self.client : interactions.Client = client

    @interactions.extension_component("TakeService")
    async def TakeService(self, ctx: interactions.ComponentContext):
        message = ctx.message
        data = await getData(collection="services", searchValue = {"_id":int(ctx.author.id)})
        if data == None:
            await addData(collection="services", document={"_id": int(ctx.author.id), "startTime": int(time.time())})
            await ctx.send(embeds=[new_notify_embed("Bienvenue en service !")], ephemeral=True)
            embed:interactions.Embed = message.embeds[0]
            embed.fields[0].value = await getCount(collection="services")
            await message.edit(embeds=[embed], components=compos)
        else:
            await ctx.send(embeds=[create_error_embed(f"Vous avez déjà un service en cours. Vous l'avez lancé à <t:{data['startTime']}:t>")], ephemeral=True)
            return
    
    @interactions.extension_component("StopService")
    async def StopService(self, ctx: interactions.ComponentContext):
        message = ctx.message
        data = await getData(collection="services", searchValue = {"_id":int(ctx.author.id)})
        if data == None:
            await ctx.send(embeds=[create_error_embed("Vous n'êtes pas en service.")], ephemeral=True)
        else:
            ctime = int(time.time())-data["startTime"]
            print(ctime)
            savedData = await getData(collection="servicesSaved", searchValue={"_id": int(ctx.author.id)})
            if not savedData:
                await addData(collection="servicesSaved", document={"_id": int(ctx.author.id), "passedTime": 0})
                savedData = await getData(collection="servicesSaved", searchValue={"_id": int(ctx.author.id)})
            await updateData(collection="servicesSaved", filters=savedData, document={"$set":{"passedTime": savedData["passedTime"] + ctime}})
            await deleteData(collection="services", searchValue={"_id": int(ctx.author.id)})
            embed = message.embeds[0]
            embed.fields[0].value = await getCount(collection="services")
            await message.edit(embeds=embed, components=compos)
    @interactions.extension_command(
        name="sendservice",
    )
    async def sendservice(self, ctx: interactions.CommandContext):
        channel = await ctx.get_channel()
        await channel.send(
            embeds=[
                new_embed(
                    title="Service",
                    description="Prenez/arrêtez votre service avec le bouton çi-dessous.\nIl permets de vous octroyer le rôle En jeu, ainsi que de compter votre temps.",
                    color=0xb39317,
                    fields=[["Modérateurs en jeu", await getCount(collection="services"), False]]
                )
            ],
            components=compos
        )
        await ctx.send(embeds=[new_notify_embed("Le système de service est désormais actif.")])

def setup(client):
    Extension(client)