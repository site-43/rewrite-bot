import interactions

from utils.embeds import new_embed, new_notify_embed
from utils.logs import new_log

class Help(interactions.Extension):
    @interactions.extension_command(name="help", description="Montre toutes les commandes du bot")
    async def help(self, ctx: interactions.CommandContext):
        embed = new_embed(
            title="Aide",
            footer_text="Contacte @Saturna19#1510 pour avoir plus de renseignements si nécessaire !",
        )
        for command in self.client._commands:
            if command.type == interactions.ApplicationCommandType.CHAT_INPUT:
                embed.add_field(name=f"{command.name}", value=command.description)

        await ctx.send(embeds=[embed], ephemeral=True)
        await new_log(self.client, "test", 1063194130064359545, embeds=[new_notify_embed("test")])


def setup(client: interactions.Client):
    Help(client)