import interactions

from utils.embeds import new_embed


class Help(interactions.Extension):
    @interactions.extension_command(name="help", description="Montre toutes les commandes du bot")
    async def help(self, ctx: interactions.CommandContext):
        embed = new_embed(
            title="Aide",
            color=0xFF0000,
            footer_text="Contacte @Saturna19#1510 pour avoir plus de renseignements si nécessaire !",
        )
        for command in self.client._commands:
            if command.type == interactions.ApplicationCommandType.CHAT_INPUT:
                embed.add_field(name=f"</{command.name}:0>", value=command.description)

        await ctx.send(embeds=[embed], ephemeral=True)


def setup(client: interactions.Client):
    Help(client)