import interactions
from asyncio import sleep
from utils.embeds import create_error_embed, new_notify_embed, new_embed
from utils.components import add_button, modals
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
            channel = interactions.Channel(**await self.client._http.get_channel(int(ctx.channel_id)), _client=self.client._http)
            await channel.delete()
        else:
            await ctx.send(ephemeral=True, embeds=[create_error_embed("Vous n'avez pas la permission suffisante.")])


    @interactions.extension_listener(name="on_start")
    async def on_start(self):
        presence = interactions.ClientPresence(
            activities=[
                interactions.PresenceActivity(
                    name=f"ce n'est qu'un au-revoir...",
                    type=interactions.PresenceActivityType.LISTENING,
                )
            ],
            status=interactions.StatusType.DND,
        )
        await self.client.change_presence(presence=presence)
        print("[INFO] Bot start.")
    

    @interactions.extension_listener(name="on_message_create")
    async def on_message_create(self, message:interactions.Message):
        if message.channel_id == 1096863271987982458:
            thread = await message.create_thread(name="Avis", reason="Ouverture d'un thread pour récolter les avis.")
            await thread.send(embeds=[new_embed(title="Bienvenue dans ce thread", description="Ce thread a été automatiquement généré pour discuter des propositions de la V2.", footer_text="N'hésitez pas à réagir a la proposition ! ;)")], components=[interactions.Button(label="Fermer", style=interactions.ButtonStyle.DANGER, custom_id="satu_close_thread")])
            return
    #     else:
    #         channel:interactions.Channel = await message.get_channel()
    #         messagecontent:str = message.content
    #         if channel.type == interactions.ChannelType.DM and messagecontent.find("!alphatester") != -1:
    #             await message.reply(
    #                 "Bienvenue !\nJ'apprécie le fait que tu veuilles rejoindre les testeurs de la Pré-Refonte !\nClique sur le bouton en dessous pour remplir le formulaire !",
    #                   components=[
    #                       add_button(label="Rejoindre les testeurs !", emoji=interactions.Emoji(name="💻"), custom_id="tester_submit")
    #                   ]
    #             )
    
    # @interactions.extension_component("tester_submit")
    # async def tester(self, ctx: interactions.ComponentContext):
    #     await ctx.popup(modals["Recrutements Testeur Pré-Refonte"])

    # @interactions.extension_modal("recrutement_testers")
    # async def recrutement_testers(self, ctx: interactions.ComponentContext, rec_test_pseudo_rbx:str, rec_test_motiv:str):
    #     user: interactions.User = await interactions.get(self.client, interactions.User, object_id=ctx.message.mentions[0]["id"])
    #     await ctx.message.edit("Merci d'avoir candidaté !")
    #     await ctx.send("Votre candidature a bien été envoyée.", ephemeral=True)
    #     channelREC: interactions.Channel = await interactions.get(self.client, interactions.Channel, object_id=1102608014323765288)
    #     if channelREC:
    #         post = await channelREC.create_forum_post(
    #             name=user.username,
    #             content=f"Une nouvelle candidature a été reçue.\n\n```\nNom de l'utilisateur: {user.username}\nIdentifiant: {user.id}\n\nRéponses:\nPseudo Roblox: {rec_test_pseudo_rbx}\nMotivations: {rec_test_motiv} ```",
    #         )
    #         await sleep(10)
    #         print("TAGSSSS: ", post.applied_tags)
    #     else:
    #         raise interactions.LibraryException(message="Issue when finding the channel.", severity=50)
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