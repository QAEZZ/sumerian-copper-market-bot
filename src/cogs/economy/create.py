import discord
from discord.ext import commands
from constants import EMBED_COLOR
from helpers import errorEmbed, db
from econ_types.trader import Trader

import sqlite3


class EconomyCreate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create(self, ctx):
        try:
            result = db.get_trader(ctx.author.id)

            embed: discord.Embed = discord.Embed(color=EMBED_COLOR)
            embed.set_thumbnail(url=ctx.author.avatar)

            if result:

                embed.title = "Trader already exists!"
                embed.add_field(name="User ID", value=f'```{result.user_id}```', inline=False)
                embed.add_field(name="Low Grade Bal", value=f'```{result.low_grade_balance}```', inline=False)
                embed.add_field(name="Medium Grade Bal", value=f'```{result.medium_grade_balance}```', inline=False)
                embed.add_field(name="High Grade Bal", value=f'```{result.high_grade_balance}```', inline=False)


                await ctx.reply(embed=embed)
            else:
                new_bronze_trader = Trader(user_id=ctx.author.id, bal_low_grade=100, bal_medium_grade=0, bal_high_grade=0)
                db.create_trader(new_bronze_trader)

                embed.title = "Trader Created!"
                embed.add_field(name="Low Grade Bal", value='```100```', inline=False)
                embed.add_field(name="Med Grade Bal", value='```0```', inline=False)
                embed.add_field(name="High Grade Bal", value='```0```', inline=False)

                await ctx.reply(embed=embed)

        except Exception as e:
            await errorEmbed.send(ctx, e)


async def setup(bot):
    await bot.add_cog(EconomyCreate(bot))