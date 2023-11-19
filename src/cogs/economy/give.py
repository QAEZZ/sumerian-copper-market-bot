import discord
from constants import EMBED_COLOR, LOGO, PREFIX
from discord.ext import commands
from econ_types.trader import Trader
from helpers import db, errorEmbed


class EconomyGive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _check_balance(
        self, trader: Trader, grade_type: str, amount: int
    ) -> tuple[bool, str]:
        if grade_type == 'high' and amount > trader.high_grade_balance:
            return (False, 'Trader, you are too broke!')

        elif grade_type == 'medium' and amount > trader.medium_grade_balance:
            return (False, 'Trader, you are too broke!')

        elif grade_type == 'low' and amount > trader.low_grade_balance:
            return (False, 'Trader, you are too broke!')

        return (True, 'All OK')

    @commands.command()
    async def give(
        self,
        ctx,
        member: discord.Member = None,
        grade_type: str = None,
        amount: int = None,
    ):
        try:
            if (
                member is None
                or grade_type is None
                or amount is None
                or grade_type.lower() not in ['low', 'medium', 'high']
            ):
                await errorEmbed.send(
                    ctx,
                    f'Incorrect usage!\n\nEx.\n{PREFIX}give <member> <grade_type> <amount>\n\nGrade types:\nlow\nmedium\nhigh',
                    False,
                )
                return

            if member.id == ctx.author.id:
                await errorEmbed.send(
                    ctx, "Trader, you can't give yourself your own bronze.", False
                )
                return

            grade_type = grade_type.lower()

            embed: discord.Embed = discord.Embed(color=EMBED_COLOR)
            embed.set_thumbnail(url=LOGO)

            author_result = db.get_trader(ctx.author.id)
            if not author_result:
                embed.title = "Couldn't find you, Trader!"
                embed.description = f'Did you run `{PREFIX}create`?'

                await ctx.reply(embed=embed)
                return

            trade_with_result = db.get_trader(member.id)
            if not trade_with_result:
                embed.title = f"Couldn't find {member.name}, Trader!"
                embed.description = f'Did {member.mention} run `{PREFIX}create`?'

                await ctx.reply(embed=embed)
                return

            author_balance_check = self._check_balance(
                author_result, grade_type, amount
            )
            if not author_balance_check[0]:
                embed.title = f'Uh oh, Trader!'
                embed.description = author_balance_check[1]

                await ctx.reply(embed=embed)
                return

            if grade_type == 'high':
                update_author = db.update_trader(
                    ctx.author.id, high_grade_balance=author_result.high_grade_balance - amount)
                
                update_trade_with = db.update_trader(
                    member.id, high_grade_balance=trade_with_result.high_grade_balance + amount)
            
            elif grade_type == 'medium':
                update_author = db.update_trader(
                    ctx.author.id, medium_grade_balance=author_result.medium_grade_balance - amount)
                
                update_trade_with = db.update_trader(
                    member.id, medium_grade_balance=trade_with_result.medium_grade_balance + amount)
            
            elif grade_type == 'low':
                update_author = db.update_trader(
                    ctx.author.id, low_grade_balance=author_result.low_grade_balance - amount)
                
                update_trade_with = db.update_trader(
                    member.id, low_grade_balance=trade_with_result.low_grade_balance + amount)
                
            if update_author is not True:
                embed.title = 'Uh oh, Trader!'
                embed.description = 'There was an error updating your balance!'

                await ctx.reply(embed=embed)
                return
            
            if update_trade_with is not True:
                embed.title = 'Uh oh, Trader!'
                embed.description = f"There was an error updating {member.mention}'s balance!"

                await ctx.reply(embed=embed)
                return

            embed.title = f'Gave copper to fellow Mesopotamian trader!'
            embed.description = f'Gave `{amount}` {grade_type}-grade copper to {member.mention}!'
            await ctx.reply(embed=embed)

        except Exception as e:
            await errorEmbed.send(ctx, e)


async def setup(bot):
    await bot.add_cog(EconomyGive(bot))
