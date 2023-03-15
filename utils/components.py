import interactions
from utils.embeds import create_error_embed
def add_button(
    type:interactions.ButtonStyle = interactions.ButtonStyle.PRIMARY,
    label:str = "Undefined",
    emoji:str = None,
    custom_id:str = None,
    Disabled:bool = False,
)-> interactions.Button:
    bouton = interactions.Button(
        style=type,
        label=label,
        custom_id=custom_id,
        emoji = emoji,
        disabled = Disabled
    )
    return bouton