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
                    name="Low Grade Copper Bal",
                    value=f"```{result.low_grade_balance:,}```",
                    inline=False,
                )
                embed.add_field(
                    name="Medium Grade Copper Bal",
                    value=f"```{result.medium_grade_balance:,}```",
                    inline=False,
                )
                embed.add_field(
                    name="High Grade Copper Bal",
                    value=f"```{result.high_grade_balance:,}```",
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
    
    
    @commands.command(aliases=['lb'])
    async def leaderboard(self, ctx, grade: str = 'high'):
        try:
            allowed_grades = ['low', 'medium', 'high', 'all']
            grade = grade.lower()
            
            if grade not in allowed_grades:
                await errorEmbed.send(ctx, f"Incorrect usage!\n\nTypes:\nlow\nmedium\nhigh\nall\n\nEx.\n{PREFIX}lb [type: default 'high']", False)
                return

            if grade == 'all':
                query = "SELECT * FROM traders ORDER BY (low_grade_balance + medium_grade_balance + high_grade_balance) DESC LIMIT 10"
            else:
                query = f"SELECT * FROM traders ORDER BY {grade}_grade_balance DESC LIMIT 10"

            initial_result = db.execute_raw_sql(query)

            if initial_result:
                embed: discord.Embed = discord.Embed(
                    title=f"Top 10 for {grade}{'-grade balance' if grade != 'all' else ' balances'}.",
                    color=EMBED_COLOR
                )
                embed.set_thumbnail(url=LOGO)
                if grade == 'all': embed.set_footer(text="NOTICE: 'all' balances can be swayed by putting all your balances to low-grade.")

                results = db.execute_raw_sql(query, fetch=True)

                counter = 1
                for index, result in enumerate(results, start=1):
                    user_id, low_grade, medium_grade, high_grade = result[1], result[2], result[3], result[4]
                    if grade == 'all':
                        total_balance = low_grade + medium_grade + high_grade
                    else:
                        get_trader_result = db.get_trader(user_id)
                        if not isinstance(get_trader_result, Trader):
                            await errorEmbed.send(ctx, f"There was an issue with getting trader `{user_id}`", False)
                            return
                        
                        total_balance = getattr(get_trader_result, f'{grade}_grade_balance', 'ERROR')
                    
                    user = await self.bot.fetch_user(user_id)
                    embed.add_field(name=f"{counter}. {user.name}", value=f"```{total_balance:,}```")

                    counter += 1

                await ctx.reply(embed=embed)
            else:
                await errorEmbed.send(ctx, "Error fetching leaderboard.", False)
        
        except Exception as e:
            await errorEmbed.send(ctx, e)
    


async def setup(bot):
    await bot.add_cog(EconomyBal(bot))
