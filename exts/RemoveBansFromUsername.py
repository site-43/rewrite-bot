import interactions
import asyncio
from configs import LOGSTAFF
from interactions.ext import molter
from utils.embeds import new_notify_embed, create_error_embed, new_embed
from utils.logs import new_log
from colorama import Fore

class Extension(molter.MolterExtension):
    def __init__(self, client):
        self.client = client

    @molter.prefixed_command(name="unban")
    async def removebans(self, ctx: molter.MolterContext, *, name: str):
        await new_log(self.client, channel=LOGSTAFF, embeds=[new_embed(title="Unban", description=f"{ctx.author.mention} a lancé la commande unban.")])
        if ctx.guild_id == None:
            await ctx.send(embeds=[
                create_error_embed("Cette commande n'est pas utilisable en Messages Privés.")
            ])
            return
        perms = await ctx.member.get_guild_permissions()
        if not perms & interactions.Permissions.ADMINISTRATOR == interactions.Permissions.ADMINISTRATOR:
            await ctx.send(embeds=[create_error_embed("Vous n'avez pas la permission d'executer cette commande.")])
            return
        else:
            print(perms)
        try:
            bans = await ctx.guild.get_all_bans()
        except:
            await ctx.send(embeds=[create_error_embed("Un problème est survenu. Veuillez en référer à Saturna19 le plus vite possible.")])
            return
        message = await ctx.send(embeds=[new_notify_embed("Le traitement est en cours.")])
        found = []
        errors = []
        for ban in bans:
            username = ban["user"].username
            if not username.find(name) == -1:
                found.append(ban["user"].id)
        if len(found) == 0:
            await message.edit(embeds=[create_error_embed("La recherche de bans avec ce nom d'utilisateur n'a rien donné.")])
            return
        await ctx.reply(embeds=[new_notify_embed(f"J'ai trouvé {len(found)} personne(s) à unban.\n<a:loading:1086257424534605975> Temps estimé des opérations: {(len(found)*2)} secondes")])
        for item in found:

            try:
                await asyncio.sleep(2) #Pour avoid les ratelimits.
                await ctx.guild.remove_ban(item, f"Unban par {ctx.author.name}:{ctx.author.id}")
                print(f"{Fore.YELLOW}[:: Unban ::] {ctx.author.name} a unban l'id {Fore.CYAN}{item}{Fore.RESET}")
            except:
                errors.append(item)
        ##print("LENGTH:", len(errors))
        if len(errors) == 0:
            await ctx.send(embeds=[
                new_notify_embed(f"Tout s'est bien déroulé, j'ai pu unban {len(found)} personnes comportant les caractères `{name}` à la suite dans leur pseudonyme.")
            ])
            await new_log(self.client, channel=LOGSTAFF, embeds=[new_embed(title="Unban", description=f"{ctx.author.mention} a unbanni {len(found)} utilisateurs.")])
        else:
            await ctx.send(embeds=[
                create_error_embed("Je n'ai pas réussi a unban tous les comptes. Veuillez vous référer à la console pour obtenir les identifiants non bannis.")
            ])
            [print(f"{Fore.RED}[:: Unban ::] {error} {Fore.RESET}") for error in errors]

def setup(client):
    Extension(client)