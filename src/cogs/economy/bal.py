import discord
from discord.ext import commands
from constants import EMBED_COLOR, PREFIX, LOGO
from helpers import errorEmbed
from econ_types.trader import Trader, db_create_trader

import sqlite3


class EconomyBal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bal(self, ctx, member: discord.Member = None):
        try:
            member = member or ctx.author

            conn = sqlite3.connect("db/traders.db")
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM traders WHERE user_id=?", (member.id,))
            result = cursor.fetchone()

            embed = discord.Embed(color=EMBED_COLOR)

            if result:
                embed.set_thumbnail(url=member.avatar)
                embed.title = f"Hello, Fellow Mesopotamian Copper Trader!"
                embed.add_field(name="Low Grade Bal", value=f'```{result[2]}```', inline=False)
                embed.add_field(name="Med Grade Bal", value=f'```{result[3]}```', inline=False)
                embed.add_field(name="High Grade Bal", value=f'```{result[4]}```', inline=False)

                await ctx.reply(embed=embed)
            else:
                embed.title = "Couldn't find trader!"
                embed.description = f'Did {member.mention} run `{PREFIX}create`?'
                embed.set_thumbnail(url=LOGO)

                await ctx.reply(embed=embed)

            conn.close()

        except Exception as e:
            await errorEmbed.send(ctx, e)


async def setup(bot):
    await bot.add_cog(EconomyBal(bot))