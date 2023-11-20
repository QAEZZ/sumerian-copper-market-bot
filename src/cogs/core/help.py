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
> `create` : Become a trader
> `bal` : Shows your balance
> `mine` : Go to the mines
> `beg` : No one likes a begger
> `gamble` : Gamble away your copper <:PRAISEDALORD:1079102735011557407>
> `give` : Give money to someone
> `ask` : Ask Ea-Nasir something
> `rps` : Play RPS with Ea-Nasir, place bets even

**Market Mod Tools**
> `reset` : Reset a user's balance
> `delete` : Delete a user
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