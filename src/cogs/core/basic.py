import json

import discord
from constants import EMBED_COLOR, LOGO, PREFIX, HELP_DESCRIPTION
from discord.ext import commands
from helpers import errorEmbed


class CoreHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, command_name = None):
        try:
            embed: discord.Embed = discord.Embed(
                title="Sumerian Copper Market",
                color=EMBED_COLOR,
                description=HELP_DESCRIPTION,
            )
            embed.set_thumbnail(url=LOGO)

            if command_name:
                with open("data/help.json", "r") as file:
                    help_data = json.load(file)

                    command_info = help_data.get(command_name.lower())
                    if command_info:
                        embed.title = f"Help for command {command_name}"
                        embed.description = command_info["description"]
                        embed.add_field(
                            name="Usage", value=f"```{PREFIX}{command_info['usage']}```"
                        )

            await ctx.reply(embed=embed)

        except Exception as e:
            await errorEmbed.send(ctx, e)

    @commands.command()
    async def info(self, ctx):
        embed: discord.Embed = discord.Embed(color=EMBED_COLOR)
        embed.add_field(name="Wrapper", value="```discord.py```")
        embed.add_field(name="Creator", value="```qaezz.dev```")

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(CoreHelp(bot))
