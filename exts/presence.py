import interactions
from replit import db
from configs import OWNER_ID, ABSENCECHANNEL
from utils.embeds import new_embed, create_error_embed
from utils.components import add_button
import datetime
import asyncio

absmodal = interactions.Modal(
            title="Absence",
            custom_id="abs_requests",
            components=[
                interactions.TextInput(
                    style=interactions.TextStyleType.PARAGRAPH,
                    label="Raison d'absence",
                    custom_id="abs_requests_reason",
                    placeholder="Veuillez entrer la raison ici.",
                    required=True,
                ),

                interactions.TextInput(
                    style=interactions.TextStyleType.SHORT,
                    label="Veuillez entrer la date de votre départ.",
                    custom_id="abs_requests_depart_date",
                    placeholder="Sous le format DD/MM/YYYY",
                    min_length=10,
                    max_length=10,
                    required=True,
                ),

                interactions.TextInput(
                    style=interactions.TextStyleType.SHORT,
                    label="Veuillez entrer la date de votre retour.",
                    custom_id="abs_requests_retour_date",
                    placeholder="Sous le format DD/MM/YYYY",
                    min_length=10,
                    max_length=10,
                    required=True,
                ),
            ],
        )


prmodal = interactions.Modal(

            title="Presence Réduite",

            custom_id="pr_modal",

            components=[
                interactions.TextInput(
                    style=interactions.TextStyleType.PARAGRAPH,
                    label="Raison de présence réduite.",
                    custom_id="pr_modal_reason",
                    placeholder="Veuillez entrer la raison ici.",
                    required=True,
                ),

                interactions.TextInput(
                    style=interactions.TextStyleType.SHORT,
                    label="Veuillez entrer la date de votre départ.",
                    custom_id="pr_modal_depart",
                    placeholder="Sous le format DD/MM/YYYY",
                    min_length=10,
                    max_length=10,
                    required=True,
                ),

                interactions.TextInput(
                    style=interactions.TextStyleType.SHORT,
                    label="Veuillez entrer la date de votre retour.",
                    custom_id="pr_modal_retour",
                    placeholder="Sous le format DD/MM/YYYY",
                    min_length=10,
                    max_length=10,
                    required=True,

                ),

            ],

        )

class absenceManager(interactions.Extension):

    def __init__(self, client):

        self.client: interactions.Client = client

    @interactions.extension_component("abs_request_sender")
    async def btnabs(self, ctx: interactions.CommandContext):
      await ctx.popup(absmodal)

    @interactions.extension_component("pr_request_sender")
    async def btnpr(self, ctx: interactions.ComponentContext):
      await ctx.popup(prmodal)

    @interactions.extension_component("accept1")
    async def accept1(self, ctx: interactions.ComponentContext):
      GuildMember = await ctx.guild.get_member(str(ctx.message.content).split(" ")[0])
      await GuildMember.add_role(758365326961803385)
      await ctx.send("Le rôle Absence a été ajouté.")
    
    @interactions.extension_component("accept2")
    async def accept2(self, ctx: interactions.ComponentContext):
      GuildMember = await ctx.guild.get_member(str(ctx.message.content).split(" ")[0])
      await GuildMember.add_role(912700941722091530)
      await ctx.send("Le rôle Présence Réduite a été ajouté.")

    @interactions.extension_component("refuse1")
    async def refuse1(self, ctx: interactions.ComponentContext):
      await ctx.send("**Absence refusée** - Vous avez refusé cette absence.")

    @interactions.extension_component("refuse2")
    async def refuse2(self, ctx: interactions.ComponentContext):
      await ctx.send("**Présence réduite refusée** - Vous avez refusé cette présence réduite.")

    @interactions.extension_modal('abs_requests')
    async def absmodalcb(self, ctx: interactions.CommandContext, abs_requests_reason: str, abs_requests_depart_date: str, abs_requests_retour_date: str):
            print('Received.')
            try:
                departdate = str(datetime.datetime.strptime(abs_requests_depart_date, "%d/%m/%Y").timestamp()).split(".")[0]
                retourdate = str(datetime.datetime.strptime(abs_requests_retour_date, "%d/%m/%Y").timestamp()).split(".")[0]
            except ValueError:
                departdate = abs_requests_depart_date
                retourdate = abs_requests_retour_date

            if not abs_requests_depart_date.find("/"):
                await ctx.send("Veuillez entrer correctement la(les) valeur.", ephemeral=True)
                return False

            if not abs_requests_retour_date.find("/"):
                await ctx.send("Veuillez entrer correctement la(les) valeur.", ephemeral=True)
                return False


            embed = interactions.Embed(

                title=f"Absence de: de {ctx.author.id}",

                description=f"**Une nouvelle absence a été signalée par {ctx.author.mention}**",

                fields=[interactions.EmbedField(

                    name="Date de départ fournie:",

                    value=f"<t:{departdate}:D>"

                ),
                interactions.EmbedField(

                    name="Date de retour fournie:",

                    value=f"<t:{retourdate}:D> (<t:{retourdate}:R>)"

                ),
                interactions.EmbedField(

                    name="Raison fournie:",

                    value=abs_requests_reason

                ),
                ])

            await ctx.send("Votre absence a bien été reçue. Votre gérant vous recontactera d'ici peu pour donner suite ou non à votre présence réduite.", ephemeral=True) #Message pour le staff qui fait l'annonce.
            channel = await interactions.get(self.client, interactions.Channel, object_id=ABSENCECHANNEL)
            await channel.send(content=f"{ctx.member.user.id} - <@!795745320629567489>", embeds=embed, components=[item3, item4])


########################################################################
        
    
    @interactions.extension_modal('pr_modal')
    async def prmodalcb(self, ctx: interactions.CommandContext, pr_modal_reason: str, pr_modal_depart: str, pr_modal_retour: str):
            print('Received.')
            if not pr_modal_depart.find("/"):
                await ctx.send("Veuillez entrer correctement la valeur.", ephemeral=True)
                return False

            if not pr_modal_retour.find("/"):
                await ctx.send("Veuillez entrer correctement la valeur.", ephemeral=True)
                return False
                
            try:
                departdate = str(datetime.datetime.strptime(pr_modal_depart, "%d/%m/%Y").timestamp()).split(".")[0]
                retourdate = str(datetime.datetime.strptime(pr_modal_retour, "%d/%m/%Y").timestamp()).split(".")[0]
            except ValueError:
                departdate = pr_modal_depart
                retourdate = pr_modal_retour




            embed = interactions.Embed(

                title=f"Présence réduite de {ctx.author.id}",

                description=f"**Une nouvelle présence réduite a été signalée par {ctx.author.mention}**",

                fields=[interactions.EmbedField(

                    name="Date de départ fournie:",

                    value=f"<t:{departdate}:D>"

                ),
                interactions.EmbedField(

                    name="Date de retour fournie:",

                    value=f"<t:{retourdate}:D> (<t:{retourdate}:R>)"

                ),
                interactions.EmbedField(

                    name="Raison fournie:",

                    value=pr_modal_reason

                ),
                ])

            await ctx.send("Votre absence a bien été reçue. Votre gérant vous recontactera d'ici peu pour donner suite ou non à votre présence réduite.", ephemeral=True) #Message pour le staff qui fait l'annonce.
            channel = await interactions.get(self.client, interactions.Channel, object_id=ABSENCECHANNEL)
            print(ctx.member.user.id)
            await channel.send(content=f"{ctx.member.user.id} - <@!795745320629567489>", embeds=embed, components=[item5, item6])


def setup(client):
  print('✅ Loading AbsenceManager')
  absenceManager(client)