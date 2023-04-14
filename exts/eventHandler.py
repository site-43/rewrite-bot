import interactions
from utils.embeds import create_error_embed, new_notify_embed
from utils.components import add_button
from configs import LogsChannel, BugThread
class Extension(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client

    @interactions.extension_listener(name="on_command_error")
    async def on_command_error(self, ctx: interactions.CommandContext, error):
        print("fired")
        channel = await interactions.get(self.client, interactions.Channel, object_id=LogsChannel)
        await channel.send(embeds=[create_error_embed(f"**COM[{ctx.command.name}]_ERR:**\n```{error}```")])

    
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