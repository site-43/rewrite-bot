import interactions
from configs import SalonAbsence, LogsAbsence
from utils.embeds import new_embed, create_error_embed
from utils.components import add_button
from utils.modals import absmodal, prmodal
from utils.database import addData, getData
import asyncio
buttonsABS = [
    add_button(style=interactions.ButtonStyle.SUCCESS, label="Accepter", emoji=interactions.Emoji(name="✅"), custom_id="accept"),
    add_button(style=interactions.ButtonStyle.DANGER, label="Refuser", emoji=interactions.Emoji(name="❌"), custom_id="refuse")
]
buttonsPR = [
    add_button(style=interactions.ButtonStyle.SUCCESS, label="Accepter", emoji=interactions.Emoji(name="✅"), custom_id="accept"),
    add_button(style=interactions.ButtonStyle.DANGER, label="Refuser", emoji=interactions.Emoji(name="❌"), custom_id="refuse")
]

gerantperroles = {
  781190476686032926 : [781190719154946068], #Rôle dev
  744252614732021780 : [781188326991724605], #Rôle Mod
  781190103699423272 : [790534072627757056 ,781190172347203585], #Rôle Anim
  828540193513406474 : [965212346949726298, 876147169420259399], #Rôle Créa
}

class absenceManager(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client

    @interactions.extension_component("abortPause")
    async def abortPause(self, ctx: interactions.ComponentContext):
      message = ctx.message
      bouton = add_button(label="Valider", custom_id="disable_temp_btn")
      validmessage = await ctx.send("Êtes vous sur de vouloir annuler cette absence/présence réduite ?", components=[bouton])
      try:
        Valid:interactions.ComponentContext = await self.client.wait_for_component(components=bouton, messages =[validmessage], timeout=20)
        if Valid.custom_id == 'disable_temp_btn':
          data = await getData(collection="absences", searchValue={"_id": int(message.id)})
          if not data:
            await ctx.send(embeds=[create_error_embed('Une erreur est survenue, les données de cette absence/PR n\'ont pas été trouvées.')])
            return
          embed = message.embeds[0]
          if embed:
            embed.color = 0x00114f
            embed.fields[1].value = "`Terminée`"
          member = await interactions.get(self.client, interactions.Member, object_id=data["member"], parent_id=ctx.guild_id)
          if data["types"] == "Absence":
            await member.remove_role(758365326961803385)
          else:
            await member.remove_role(912700941722091530)
            
          channel = await interactions.get(self.client, interactions.Channel, object_id=LogsAbsence)
          await channel.send(embeds=embed)
          await message.delete()
          await validmessage.delete()
          await ctx.send(f'La pause de <@!{data["member"]}> a été arrêtée, et a été archivée.', ephemeral=True)
      except:
        await validmessage.delete()

    @interactions.extension_component("abs_request_sender")
    async def btnabs(self, ctx: interactions.CommandContext):
      await ctx.popup(absmodal)

    @interactions.extension_component("pr_request_sender")
    async def btnpr(self, ctx: interactions.ComponentContext):
      await ctx.popup(prmodal)

    @interactions.extension_component("accept")
    async def accept1(self, ctx: interactions.ComponentContext):
      message = ctx.message
      data = await getData(collection="absences", searchValue={"_id": int(ctx.message.id)})
      if data:
        name = data["types"]
        member = await interactions.get(self.client, interactions.Member, object_id=data["member"], parent_id=ctx.guild_id)
        if data["types"] == "Absence":
          await member.add_role(758365326961803385)
        else:
          await member.add_role(912700941722091530)
        
        embed:interactions.Embed = ctx.message.embeds[0]
        embed.color = 0x00ff08
        embed.title = f"{name} autorisée de {member.user.username}"
        embed.fields[1].value = "`En cours`"
        embed.fields[2].value = ctx.author.mention
        await message.disable_all_components()
        
        await message.edit(embeds=embed, components=[add_button(label="Mettre fin", emoji=interactions.Emoji(name="🕓"), custom_id="abortPause")])
        await ctx.send(f'Vous avez accepté cette {data["types"]}', ephemeral=True)
      else:
        await ctx.send(embeds=[create_error_embed('Une erreur est survenue, les données de cette absences n\'ont pas été trouvées.')])

    @interactions.extension_component("refuse")
    async def refuse1(self, ctx: interactions.ComponentContext):
      data = await getData(collection="absences", searchValue={"_id": int(ctx.message.id)})
      if data:
        member = await interactions.get(self.client, interactions.Member, object_id=data["member"], parent_id=ctx.guild_id)
        message = ctx.message
        await ctx.send("**Demande refusée** - Vous avez refusé la demande.", ephemeral=True)
        print(message.embeds)
        embed = message.embeds[0]
        embed.color = 0xd40000
        embed.fields[1].value = "`Refusé`"
        embed.fields[2].value = ctx.author.mention
        embed.title = f"{embed.title} refusée de {member.user.username}" 
        channel = await interactions.get(self.client, interactions.Channel, object_id=LogsAbsence)
        await channel.send(embeds=embed)
        await message.delete()
      else:
        await ctx.send(embeds=[create_error_embed('Une erreur est survenue, les données de cette absence/PR n\'ont pas été trouvées.')])



    @interactions.extension_modal('abs_requests')
    async def absmodalcb(self, ctx: interactions.CommandContext, abs_requests_reason: str, abs_requests_depart_date: str, abs_requests_retour_date: str):
      embed = new_embed(title=f"Absence", description=f"**Une nouvelle absence a été signalée par {ctx.author.mention}**", fields=[["Raison", abs_requests_reason, False], ["Statut", "`En attente`", False], ["Gérant", "Non accepté", False], ["Dates", f"{abs_requests_depart_date} - {abs_requests_retour_date}", False]])
      channel = await interactions.get(self.client, interactions.Channel, object_id=SalonAbsence)
      await ctx.send("Votre absence a bien été reçue. Votre gérant vous recontactera d'ici peu pour donner suite ou non à votre présence réduite.", ephemeral=True)
      message = await channel.send(embeds=embed, components=buttonsABS)
      await addData(collection="absences", document={"_id": int(message.id), 'member': int(ctx.member.user.id), 'types': 'Absence'})
      pings = []
      for role in ctx.author.roles:
        if role in gerantperroles:
          for grole in gerantperroles[role]:
            pings.append(grole)
      if len(pings) >= 0:
        for ping in pings:
          pingmsg = await channel.send(content=f"<@&{ping}>")
          await asyncio.sleep(2)
          await pingmsg.delete()


########################################################################
    @interactions.extension_modal('pr_modal')
    async def prmodalcb(self, ctx: interactions.CommandContext, pr_modal_reason: str, pr_modal_depart: str, pr_modal_retour: str):
      embed = new_embed(title=f"Présence réduite", description=f"**Une nouvelle présence réduite a été signalée par {ctx.author.mention}**", fields=[["Raison", pr_modal_reason, False], ["Statut", "`En attente`", False], ["Gérant", "Non accepté", False], ["Dates", f"{pr_modal_depart} - {pr_modal_retour}", False]])
      channel = await interactions.get(self.client, interactions.Channel, object_id=SalonAbsence)
      await ctx.send("Votre présence réduite a bien été reçue. Votre gérant vous recontactera d'ici peu pour donner suite ou non à votre présence réduite.", ephemeral=True)
      message = await channel.send(embeds=embed, components=buttonsABS)
      await message.edit(content="", components=message.components)
      await addData(collection="absences", document={"_id": int(message.id), 'member': int(ctx.member.user.id), 'types': 'Présence réduite'})
      pings = []
      for role in ctx.author.roles:
        if role in gerantperroles:
          for grole in gerantperroles[role]:
            pings.append(grole)
      if len(pings) >= 0:
        for ping in pings:
          pingmsg = await channel.send(content=f"<@&{ping}>")
          await asyncio.sleep(2)
          await pingmsg.delete()
            

def setup(client):
  print('Loading AbsenceManager')
  absenceManager(client)