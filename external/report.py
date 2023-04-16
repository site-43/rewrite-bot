import interactions
from configs import ReportStaffChannel
class Report(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client
    
    @interactions.extension_command(
        name="report",
        description="Signalez un membre du Staff avec cette interaction.",
        dm_permission=False,
        scope=675379685869486080,
        options=[
            interactions.Option(
                type=interactions.OptionType.USER,
                name="utilisateur",
                description="Veuillez communiquer le nom du Staff à report",
                required=True,
            )
        ]
    )
    async def report(self, ctx: interactions.CommandContext, utilisateur: interactions.Member):
        modal = interactions.Modal(
        title="Formulaire de Report",
        custom_id="report_staff_form",
        components=[
            interactions.TextInput(
                style=interactions.TextStyleType.SHORT,
                label="Nom d'utilisateur (Auto)",
                custom_id="report_name",
                value=str(utilisateur.user.username + "#" + utilisateur.user.discriminator),
                required=True
            ),
            interactions.TextInput(
                style=interactions.TextStyleType.PARAGRAPH,
                label="Raison",
                custom_id="reason"
            )
        ],
    )
        await ctx.popup(modal)
        await ctx.send('Veuillez remplir le formulaire.')

    @interactions.extension_modal('report_staff_form')
    async def reportmodal(self, ctx: interactions.CommandContext, report_name: str, reason: str):
        embed = interactions.Embed(
        title="<:warningicon:1047186757675909121> Report Staff",
        description=f"Un nouveau rapport à été envoyé. \n **Raison fournie par {ctx.user.mention}**\n```{reason}```",
        url="https://bit.ly/report_staff",
        thumbnail=interactions.EmbedImageStruct(url="https://cdn.discordapp.com/attachments/1023676018256523347/1047197506255212634/3544-warning-icon.png"),
        fields=[interactions.EmbedField(name="Auteur", value=ctx.user.mention, inline=True), interactions.EmbedField(name="Membre report:", value=report_name, inline=True)]
    )
        channel = await interactions.get(self.client, interactions.Channel, object_id=ReportStaffChannel)
        await channel.send(content="<@&744252702124539925> | <@&744252806055067708>", embeds=embed)
        await ctx.send('Report envoyé', ephemeral=True)

    
        dms = interactions.Channel(**await self.client._http.create_dm(795745320629567489), _client=self.client._http)
        await dms.send(embeds=embed) #Logs
        
def setup(client):
  print('✅ Loading ReportSystem')
  Report(client)