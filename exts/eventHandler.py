import interactions
from asyncio import sleep
from utils.embeds import create_error_embed, new_notify_embed, new_embed
from utils.components import add_button
from configs import VERSION, LogsChannel
class Extension(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client

    @interactions.extension_listener(name="on_command_error")
    async def on_command_error(self, ctx: interactions.CommandContext, error):
        print(error)
        channel = await interactions.get(self.client, interactions.Channel, object_id=LogsChannel)
        await channel.send(embeds=[create_error_embed(f"**COM[{ctx.command.name}]_ERR:**\n```{error}```")])




    @interactions.extension_component("satu_close_thread")
    async def satu_close_thread(self, ctx: interactions.ComponentContext):
        owner = await interactions.get(self.client, interactions.User, object_id=self.client.me.team.owner_user_id)
        if ctx.author.id == owner.id:
            print(ctx)
            print(ctx.channel_id)
            await ctx.send(embeds=[new_notify_embed("Suppression dans 5 secondes.")],ephemeral=True)
            await sleep(5)
            channel = interactions.Channel(**await self.client._http.get_channel(ctx.channel_id), _client=self.client._http)
            await ctx.channel.delete()
        else:
            await ctx.send(ephemeral=True, embeds=[create_error_embed("Vous n'avez pas la permission suffisante.")])


    @interactions.extension_listener(name="on_start")
    async def on_start(self):
        presence = interactions.ClientPresence(
            activities=[
                interactions.PresenceActivity(
                    name=f"la version {VERSION}",
                    type=interactions.PresenceActivityType.GAME
                )
            ],
            status=interactions.StatusType.ONLINE,
        )
        await self.client.change_presence(presence=presence)
        print("[INFO] Bot start.")
    
    @interactions.extension_listener(name="on_message_create")
    async def on_message_create(self, message:interactions.Message):
        if not message.channel_id == 1096863271987982458:
            return
        thread = await message.create_thread(name="Avis", reason="Ouverture d'un thread pour récolter les avis.")
        await thread.send(embeds=[new_embed(title="Bienvenue dans ce thread", description="Ce thread a été automatiquement généré pour discuter des propositions de la V2.", footer_text="N'hésitez pas à réagir a la proposition ! ;)")], components=[interactions.Button(label="Fermer", style=interactions.ButtonStyle.DANGER, custom_id="satu_close_thread")])

    # @interactions.extension_listener(name="on_thread_create")
    # async def on_thread_create(self, Thread: interactions.Thread):
    #     if not Thread.parent_id or int(Thread.parent_id) != BugThread:
    #         return
    #     if Thread.owner_id == self.client.me.id:
    #         return
    #     print(type(Thread))
    #     await Thread.send(embeds=[new_notify_embed("Si vous avez besoin de plus d'aide de la part du développement, vous pouvez cliquer ici.")], components=[add_button(style=interactions.ButtonStyle.SUCCESS, label="Demander de l'aide", custom_id="CallHelp")])
    #     # for LThread in ListenedThreads:
        #     if LThread == int(Thread.parent_id):
        #         await Thread.send("Found")
    # @interactions.extension_component("ee")
    # async def ee(self, ctx: interactions.ComponentContext):
    #     await ctx.channel.modify
        

def setup(client):
    Extension(client)