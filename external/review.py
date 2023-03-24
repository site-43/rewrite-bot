import interactions
## A REVIEW COMMAND FOR LYS LABS BOT.
from utils.embeds import new_embed, new_notify_embed
from configs import products, rates

class review(interactions.Extension):
    def __init__(self, client):
        self.client = client

    @interactions.extension_command(
        name="review",
        description="Review our product.",
        options = [
            interactions.Option(
                name="product",
                type=interactions.OptionType.STRING,
                description="Product name",
                required=True,
                choices=[interactions.Choice(name=product, value=product) for product in products]
            ),
            interactions.Option(
                name="text",
                description="Your opinion on the product.",
                required=True,
                type=interactions.OptionType.STRING,
            ),
            interactions.Option(
                name="stars",
                description="How many stars do you give to the product ?",
                type=interactions.OptionType.STRING,
                required=True,
                choices=[interactions.Choice(name=rate, value=rate) for rate in rates]
            )
        ])
    async def review(self, ctx, product:str, text:str, stars:str):
        embed = new_embed(
            title="New review",
            description=f"{ctx.author.mention} added a review to the product {product}\n{text}",
            fields=["Rate", stars, False],
            )
        channel = await interactions.get(self.client, interactions.Channel, 1078994922058817536)
        await channel.send(embeds=[embed])

def setup(client):
    review(client)