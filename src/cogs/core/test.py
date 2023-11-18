import discord
from discord.ext import commands
from constants import EMBED_COLOR


class CoreTest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        embed: discord.Embed = discord.Embed(
            title=f"I am working.", color=EMBED_COLOR
        )
        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(CoreTest(bot))
