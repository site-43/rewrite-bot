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
    ]),
    "Recrutements Testeur Pré-Refonte": interactions.Modal(custom_id="recrutement_testers", title="Devenir testeur", components=[
        interactions.TextInput(
            style=interactions.TextStyleType.SHORT,
            label="Pseudonyme Roblox",
            required=True,
            custom_id="rec_test_pseudo_rbx"
            ),
        interactions.TextInput(
            style=interactions.TextStyleType.PARAGRAPH,
            label="Vos motivations",
            required=True,
            custom_id="rec_test_motiv"
        )
    ]),
    "Proposition Admin": interactions.Modal(custom_id="admin_propose", title="Proposer un sujet", components=[
        interactions.TextInput(
            style=interactions.TextStyleType.SHORT,
            label="Nom du sujet",
            required=True,
            custom_id="propositionName",
            max_length=100,
            min_length=2,
            placeholder="Le nom du sujet que vous voulez proposer.",
        ),
        interactions.TextInput(
            style=interactions.TextStyleType.PARAGRAPH,
            label="Description du sujet",
            required=True,
            custom_id="propositionDescription",
            max_length=2048,
            min_length=5,
            placeholder="La description du sujet que vous voulez proposer.",
        )
    ])
}