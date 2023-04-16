import interactions
from utils.embeds import create_error_embed
def add_button(
    style:interactions.ButtonStyle = interactions.ButtonStyle.PRIMARY,
    label:str = "Undefined",
    emoji:interactions.Emoji = None,
    custom_id:str = None,
    Disabled:bool = False,
)-> interactions.Button:
    bouton = interactions.Button(
        style=style,
        label=label,
        custom_id=custom_id,
        emoji = emoji,
        disabled = Disabled
    )
    return bouton

modals = {
    "AffiliatedMessage": interactions.Modal(custom_id="AffiliatedMessage", title="Message affilié", components=[
        interactions.TextInput(
            style=interactions.TextStyleType.PARAGRAPH,
            label="Message",
            custom_id="affiliatedMsg",
            required=True
            )
    ]),
    "SayMessage": interactions.Modal(custom_id="say_msg", title="Envoyer un message", components=[
        interactions.TextInput(
            style=interactions.TextStyleType.SHORT,
            label="SalonID (si nécessaire)",
            required=False,
            placeholder="L'identifiant du salon dans lequel envoyer le message (Optionnel)",
            custom_id="say_channel"
        ),
        interactions.TextInput(
            style=interactions.TextStyleType.PARAGRAPH,
            label='Message à envoyer',
            required=True,
            placeholder="Le message que vous voulez envoyer.",
            max_length=2048,
            custom_id="say_text"
        )
    ])
}