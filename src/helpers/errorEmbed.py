from discord import Embed, Color
from constants import LOGO

async def send(ctx, e):
    print(e)
    embed: Embed = Embed(
        description=f"```{e}```", color=Color.from_rgb(255,100,100)
    )
    embed.set_thumbnail(url=LOGO)
    await ctx.reply(embed=embed)