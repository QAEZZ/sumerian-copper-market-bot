import discord
from constants import EMBED_COLOR, LOGO, PREFIX
from discord.ext import commands
from econ_types.trader import Trader
from helpers import db, errorEmbed


class EconomyBal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bal(self, ctx, member: discord.Member = None):
        try:
            member = member or ctx.author

            result = db.get_trader(member.id)

            embed = discord.Embed(color=EMBED_COLOR)

            if result:
                embed.set_thumbnail(url=member.avatar)
                embed.title = f"Hello, Fellow Mesopotamian Copper Trader!"
                embed.add_field(
                    name="Low Grade Bal",
                    value=f"```{result.low_grade_balance}```",
                    inline=False,
                )
                embed.add_field(
                    name="Medium Grade Bal",
                    value=f"```{result.medium_grade_balance}```",
                    inline=False,
                )
                embed.add_field(
                    name="High Grade Bal",
                    value=f"```{result.high_grade_balance}```",
                    inline=False,
                )

                await ctx.reply(embed=embed)
            else:
                embed.title = "Couldn't find trader!"
                embed.description = f"Did {member.mention} run `{PREFIX}create`?"
                embed.set_thumbnail(url=LOGO)

                await ctx.reply(embed=embed)

        except Exception as e:
            await errorEmbed.send(ctx, e)


async def setup(bot):
    await bot.add_cog(EconomyBal(bot))
