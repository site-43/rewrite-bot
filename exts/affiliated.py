import interactions

from utils.embeds import new_embed, new_notify_embed, create_error_embed
from utils.database import getAllData, getData
from utils.components import add_button, modals

class Extension(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client

    @interactions.extension_component("send_msg_in_affiliated")
    async def send_affiliated(self, ctx:interactions.ComponentContext):
        embed = ctx.message.embeds[0]
        serverID = int(ctx.message.embeds[0].fields[0].value)
        if not serverID:
            return
        server = await getData(collection="configs", searchValue={"_id": serverID})
        if not server:
            return
        components = [add_button(style=interactions.ButtonStyle.PRIMARY, label="Message Global", emoji=interactions.Emoji(name="📣"), custom_id="global_msg_affiliated")]
        msg = await ctx.send(embeds=[embed], components=components, ephemeral=True)
        try:
            waitfor:interactions.ComponentContext = await self.client.wait_for_component(components=components, messages=msg, timeout=20)
            if waitfor.custom_id == "global_msg_affiliated":
                #await msg.disable_all_components()
                # await ctx.send("Ca marche yaaaaa") # A FINIR: - Recup Salon - Demander le message -Demander si mentions - Envoyer dans le salon
                await waitfor.popup(modal=modals["AffiliatedMessage"])
                try:
                    affimsg, fields = await self.client.wait_for_modal(modals=modals["AffiliatedMessage"], timeout=100)
                    print(fields)
                    cmessage = await affimsg.send(embeds=[new_notify_embed("L'envoi du message est en cours")], ephemeral=True)
                    channel = await interactions.get(self.client, interactions.Channel, object_id=server["announcementGlobal"])
                    if channel:
                        try:
                            await channel.send(fields[0])
                            print("here")
                            await affimsg.send(embeds=[new_notify_embed(f"Le message a été envoyé dans {channel.mention}.")])
                            print("here??")
                        except Exception as e:
                            await affimsg.send(embeds=[create_error_embed("Le message n'a pas pu être envoyé.")])
                            print(e)
                except Exception as err:
                    await ctx.send("Vous n'avez pas soumis votre message dans les temps.", ephemeral=True)
                    print(err)
        except:
            await msg.delete()


    @interactions.extension_component("menu_component")
    async def extension(self, ctx: interactions.ComponentContext, option):
        server = await getData(collection="configs", searchValue={"_id": int(option[0])})
        if not server:
            await ctx.send(embeds=[create_error_embed("Erreur.")])
            return
        await ctx.edit(embeds=[
            new_embed(
                title=server["servername"],
                description="Voici les actions affiliés que vous pouvez faire sur ce serveur.",
                fields=[["Identifiant", str(server["_id"]), False]]
            ),
        ],
        components=[
            add_button(style=interactions.ButtonStyle.PRIMARY, label="Envoyer un message", emoji=interactions.Emoji(name="✉️"), custom_id="send_msg_in_affiliated"),
            add_button(style=interactions.ButtonStyle.SECONDARY, label="Editer l'accès des salons", emoji=interactions.Emoji(name="⚠️") , custom_id="remove_everyone_affiliated")
        ])

    @interactions.extension_command( 
        name="affiliated"
    )
    async def affiliated(self, ctx: interactions.CommandContext):
        cursor = await getAllData(collection="configs", searchValue={})
        print(cursor)
        servers = {} # Dictionnaire qui stockera les noms et identifiants de serveurs

        for data in cursor:
            servers[data["servername"]] = {"sid": data["_id"]}

        options = [] # Liste qui stockera les options pour chaque nom de serveur et identifiant de serveur

        for servername, serverinfo in servers.items():
            option = interactions.SelectOption(
                label=servername,
                value=str(serverinfo["sid"])
            )
            options.append(option)

        await ctx.send(
            components=[
                interactions.SelectMenu(
                    options=options,
                    placeholder="Sélectionnez le serveur dans lequel vous avez besoin d'intéragir.",
                    custom_id="menu_component",
                )
            ]
        )


def setup(client: interactions.Client):
    Extension(client)