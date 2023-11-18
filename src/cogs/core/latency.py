import discord
from discord.ext import commands
from constants import EMBED_COLOR


class CoreLatency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def latency(self, ctx):
        embed: discord.Embed = discord.Embed(
            title=f"Ping: {round(self.bot.latency*1000)}ms", color=EMBED_COLOR
        )
        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(CoreLatency(bot))