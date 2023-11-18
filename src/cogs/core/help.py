import discord
from discord.ext import commands
from constants import EMBED_COLOR, LOGO


class CoreHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        try:
            embed: discord.Embed = discord.Embed(
                title="Sumerian Copper Market", color=EMBED_COLOR,
                description="""
**Client Tools**
> `help` : shows this
> `latency` : shows the latency in ms

**Market Tools**
> `bal` : Shows your balance
"""
            )
            embed.set_thumbnail(url=LOGO)
            await ctx.reply(embed=embed)
        except Exception as e:
            embed: discord.Embed = discord.Embed(
                title=f"```{e}```", color=discord.Color.from_rgb(255, 100, 100)
            )
            await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(CoreHelp(bot))