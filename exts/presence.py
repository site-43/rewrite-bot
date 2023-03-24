import interactions
#from replit import db
from configs import OWNER_ID, ABSENCECHANNEL, STAFFGUILD
from utils.embeds import new_embed, create_error_embed
from utils.components import add_button
from utils.modals import absmodal, prmodal
import datetime
from colorama import Fore
import asyncio
buttonsABS = [
    add_button(type=interactions.ButtonStyle.SUCCESS, label="Accepter", emoji=interactions.Emoji(name="✅"), custom_id="accept1"),
    add_button(type=interactions.ButtonStyle.DANGER, label="Refuser", emoji=interactions.Emoji(name="❌"), custom_id="refuse")
]
buttonsPR = [
    add_button(type=interactions.ButtonStyle.SUCCESS, label="Accepter", emoji=interactions.Emoji(name="✅"), custom_id="accept2"),
    add_button(type=interactions.ButtonStyle.DANGER, label="Refuser", emoji=interactions.Emoji(name="❌"), custom_id="refuse")
]
db = {}
db["test"] = {}

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

    @interactions.extension_component("abs_request_sender")
    async def btnabs(self, ctx: interactions.CommandContext):
      await ctx.popup(absmodal)

    @interactions.extension_component("pr_request_sender")
    async def btnpr(self, ctx: interactions.ComponentContext):
      await ctx.popup(prmodal)

    @interactions.extension_component("accept1")
    async def accept1(self, ctx: interactions.ComponentContext):
      if int(ctx.message.id) in db["test"]:
        await ctx.send(f"Found. User: {db['test'][int(ctx.message.id)]['member']}")
      else:
        print("Not found", db["test"])
        print(f'{Fore.CYAN} {ctx.message.id} {Fore.RESET}')
    
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
            print('Received.')
            dates = await absenceManager.check([abs_requests_depart_date, abs_requests_retour_date])
            if not dates:
                await ctx.send("Erreur, veuillez communiquer des dates valides en suivant le format `DD/MM/YYYY`.\nExemple: `01/02/2023`", ephemeral=True)
                return


            embed = new_embed(title=f"Absence de {ctx.author.id}", description=f"**Une nouvelle absence a été signalée par {ctx.author.mention}**", fields=[["a", "b", False], ["a", "c", False]])
            channel = await interactions.get(self.client, interactions.Channel, object_id=ABSENCECHANNEL)
            await ctx.send("Votre absence a bien été reçue. Votre gérant vous recontactera d'ici peu pour donner suite ou non à votre présence réduite.", ephemeral=True) #Message pour le staff qui fait l'annonce.
            message = await channel.send(content=f"{ctx.member.user.id} - <@!795745320629567489>", embeds=embed, components=buttonsABS)


            data:dict = db["test"]
            data[int(message.id)] = {'member': int(ctx.member.user.id)}
            db["test"] = data
            print(db["test"])


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
            await ctx.send("Votre absence a bien été reçue. Votre gérant vous recontactera d'ici peu pour donner suite ou non à votre présence réduite.", ephemeral=True) #Message pour le staff qui fait l'annonce.
            
            message:interactions.Message = await channel.send(content=f"<@!795745320629567489>", embeds=[embed], components=buttonsPR)
            
            
            data:dict = db["test"]
            data[int(message.id)] = {'member': int(ctx.member.user.id)}
            db["test"] = data
            print(db["test"])
            
            
            # try:
            #     data:dict = db["test"]
            #     data.update({message.id, ctx.member.user.id})
            #     db["test"] = data
            #     print(db["test"])
            # except:
            #     print("no.")

def setup(client):
  print('✅ Loading AbsenceManager')
  absenceManager(client)