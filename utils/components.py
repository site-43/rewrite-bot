import interactions
from utils.logs import new_log
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