import discord
from discord.ext import commands
from constants import EMBED_COLOR
from helpers import errorEmbed
from econ_types.trader import Trader, db_create_trader

import sqlite3


class EconomyCreate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create(self, ctx):
        try:
            conn = sqlite3.connect("db/traders.db")
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM traders WHERE user_id=?", (ctx.author.id,))
            result = cursor.fetchone()

            embed: discord.Embed = discord.Embed(color=EMBED_COLOR)
            embed.set_thumbnail(url=ctx.author.avatar)

            if result:

                embed.title = "Trader already exists!"
                embed.add_field(name="User ID", value=f'```{result[1]}```', inline=False)
                embed.add_field(name="Low Grade Bal", value=f'```{result[2]}```', inline=False)
                embed.add_field(name="Med Grade Bal", value=f'```{result[3]}```', inline=False)
                embed.add_field(name="High Grade Bal", value=f'```{result[4]}```', inline=False)


                await ctx.reply(embed=embed)
            else:
                new_bronze_trader = Trader(user_id=ctx.author.id, init_bal_low_grade=100, init_bal_medium_grade=0, init_bal_high_grade=0)
                db_create_trader(new_bronze_trader)

                embed.title = "Trader Created!"
                embed.add_field(name="Low Grade Bal", value='```100```', inline=False)
                embed.add_field(name="Med Grade Bal", value='```0```', inline=False)
                embed.add_field(name="High Grade Bal", value='```0```', inline=False)

                await ctx.reply(embed=embed)

            conn.close()
        except Exception as e:
            await errorEmbed.send(ctx, e)


async def setup(bot):
    await bot.add_cog(EconomyCreate(bot))