import interactions
from configs import OWNER_ID, ABSENCECHANNEL, STAFFGUILD
from utils.embeds import new_embed, create_error_embed
from utils.components import add_button
from utils.modals import absmodal, prmodal
from utils.database import addData, getData
import datetime
from colorama import Fore
import math
import asyncio
import pymongo
buttonsABS = [
    add_button(style=interactions.ButtonStyle.SUCCESS, label="Accepter", emoji=interactions.Emoji(name="✅"), custom_id="accept1"),
    add_button(style=interactions.ButtonStyle.DANGER, label="Refuser", emoji=interactions.Emoji(name="❌"), custom_id="refuse")
]
buttonsPR = [
    add_button(style=interactions.ButtonStyle.SUCCESS, label="Accepter", emoji=interactions.Emoji(name="✅"), custom_id="accept2"),
    add_button(style=interactions.ButtonStyle.DANGER, label="Refuser", emoji=interactions.Emoji(name="❌"), custom_id="refuse")
]

class absenceManager(interactions.Extension):
    

    def __init__(self, client):

        self.client: interactions.Client = client
    
    async def check(values:dict = None):
        
        if values == None:
            return
        try:
            departdate = round(datetime.datetime.strptime(values[0], "%d/%m/%Y").timestamp())
            retourdate = round(datetime.datetime.strptime(values[1], "%d/%m/%Y").timestamp())
            return [departdate, retourdate]
        except:
            return False

    @interactions.extension_component("abortPause")
    async def abortPause(self, ctx: interactions.ComponentContext):
      message = ctx.message
      bouton = add_button(label="Valider", custom_id="disable_temp_btn")
      validmessage = await ctx.send("Êtes vous sur de vouloir annuler cette absence/présence réduite ?", components=[bouton])
      try:
        Valid:interactions.ComponentContext = await self.client.wait_for_component(components=bouton, messages =[validmessage], timeout=20)
        if Valid.custom_id == 'disable_temp_btn':
          data = await getData(collection="absences", searchValue={"_id": int(message.id)})
          embed = message.embeds[0]
          if embed and data:
            embed.color = 0x00114f
            embed.add_field('Statut', "Terminé")
          await message.edit(embeds=embed)
          await ctx.send(f"La pause de <@!{data['member']}> a été arrêtée ")
      except:
        await Valid.delete()

    @interactions.extension_component("abs_request_sender")
    async def btnabs(self, ctx: interactions.CommandContext):
      await ctx.popup(absmodal)

    @interactions.extension_component("pr_request_sender")
    async def btnpr(self, ctx: interactions.ComponentContext):
      await ctx.popup(prmodal)

    @interactions.extension_component("accept1")
    async def accept1(self, ctx: interactions.ComponentContext):
      message = ctx.message
      data = await getData(collection="absences", searchValue={"_id": int(ctx.message.id)})
      if data:
        member = await interactions.get(self.client, interactions.Member, object_id=data["member"], parent_id=ctx.guild_id)
        await member.add_role(1042146870446800956)
        embed:interactions.Embed = ctx.message.embeds[0]
        embed.color = 0x00ff08
        embed.title = f"Absence autorisée de {member.user.username}"
        embed.fields[1].value = "`En cours`"
        embed.fields[2].value = ctx.author.mention
        await message.disable_all_components()
        
        await message.edit(embeds=embed, components=[add_button(label="Mettre fin", emoji=interactions.Emoji(name="🕓"), custom_id="abortPause")])
      else:
        await ctx.send(embeds=[create_error_embed('Une erreur est survenue, les données de cette absences n\'ont pas été trouvées.')])
    
    @interactions.extension_component("accept2")
    async def accept2(self, ctx: interactions.ComponentContext):
      GuildMember = await ctx.guild.get_member(str(ctx.message.content).split(" ")[0])
      await GuildMember.add_role(912700941722091530)
      await ctx.send("Le rôle Présence Réduite a été ajouté.")

    @interactions.extension_component("refuse")
    async def refuse1(self, ctx: interactions.ComponentContext):
      message = ctx.message
      print("e")
      await ctx.send("**Demande refusée** - Vous avez refusé la demande.")
      print(message.embeds)
      embed = message.embeds[0]
      embed.color = 0xd40000
      await message.edit(embeds=embed)


    @interactions.extension_modal('abs_requests')
    async def absmodalcb(self, ctx: interactions.CommandContext, abs_requests_reason: str, abs_requests_depart_date: str, abs_requests_retour_date: str):
            dates = await absenceManager.check([abs_requests_depart_date, abs_requests_retour_date])
            if not dates:
                await ctx.send("Erreur, veuillez communiquer des dates valides en suivant le format `DD/MM/YYYY`.\nExemple: `01/02/2023`", ephemeral=True)
                return


            embed = new_embed(title=f"Absence", description=f"**Une nouvelle absence a été signalée par {ctx.author.mention}**", fields=[["Raison", abs_requests_reason, False], ["Statut", "En attente", False], ["Gérant", "Non accepté", False], ["Dates", f"{abs_requests_depart_date} - {abs_requests_retour_date}", False]])
            channel = await interactions.get(self.client, interactions.Channel, object_id=ABSENCECHANNEL)
            await ctx.send("Votre absence a bien été reçue. Votre gérant vous recontactera d'ici peu pour donner suite ou non à votre présence réduite.", ephemeral=True)
            message = await channel.send(content="<@!795745320629567489>", embeds=embed, components=buttonsABS)
            await addData(collection="absences", document={"_id": int(message.id), 'member': int(ctx.member.user.id), 'date': int(datetime.datetime.now().timestamp())})


########################################################################
        
    
    @interactions.extension_modal('pr_modal')
    async def prmodalcb(self, ctx: interactions.CommandContext, pr_modal_reason: str, pr_modal_depart: str, pr_modal_retour: str):
            print('Received.')
            dates = await absenceManager.check([pr_modal_depart, pr_modal_retour])
            if not dates:
                await ctx.send("Erreur, veuillez communiquer des dates valides en suivant le format `DD/MM/YYYY`.\nExemple: `01/02/2023`", ephemeral=True)
                return

            embed:interactions.Embed = new_embed(

                title=f"Présence réduite de {ctx.author.id}",

                description=f"**Une nouvelle présence réduite a été signalée par {ctx.author.mention}**",

                fields=[
                    ["Date de départ fournie:", f"<t:{dates[0]}:D>", False],
                    ["Date de retour fournie:", f"<t:{dates[0]}:D>", False],
                    ["Raison fournie:", pr_modal_reason, False],
                ]
            )
            channel = await interactions.get(self.client, interactions.Channel, object_id=ABSENCECHANNEL)
            await ctx.send("Votre absence a bien été reçue. Votre gérant vous recontactera d'ici peu pour donner suite ou non à votre présence réduite.", ephemeral=True) 
            
            message:interactions.Message = await channel.send(content=f"<@!795745320629567489>", embeds=[embed], components=buttonsPR)

def setup(client):
  print('✅ Loading AbsenceManager')
  absenceManager(client)