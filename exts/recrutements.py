import interactions
from configs import sections, sectionsDEV
class Extension(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client

    @interactions.extension_component("selector_recrutement_Developpement")
    async def selector_recrutement(self, ctx: interactions.ComponentContext, choice:str):
        await ctx.send(choice[0])
        if choice[0] == "Scripter":
            await ctx.send("E")

    @interactions.extension_command(
        name="recrutements",
        description="Modifie les recrutements",
        options=[interactions.Option(
            required=True,
            description="Le département dans lequel modifier les recrutements.",
            type=interactions.OptionType.STRING,
            name="section",
            choices=[interactions.Choice(name=sname, value=sname) for sname in sections]
        )]
    )
    async def recrutements(self, ctx:interactions.CommandContext, section:str):
        await ctx.send(content=section)
        if section == "Developpement":
            await ctx.send(components=[interactions.SelectMenu(custom_id=f"selector_recrutement_{section}", options=[interactions.SelectOption(label=splabel, value=splabel) for splabel in sectionsDEV])])
            await ctx.send("ok")

def setup(client: interactions.Client):
    Extension(client)