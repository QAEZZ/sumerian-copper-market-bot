import discord
from discord.ext import commands
from constants import EMBED_COLOR, PREFIX, LOGO, ECONOMY_MODERATOR, CLIENT_OWNER
from helpers import errorEmbed, db
from econ_types.trader import Trader

class EconomyModeration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def _moderation_access(ctx):
        if ctx.author.id in ECONOMY_MODERATOR:
            return True
        return False
    
    def _is_client_owner():
        async def predicate(ctx):
            return ctx.author.id == CLIENT_OWNER

        return commands.check(predicate)

    @commands.command()
    @_is_client_owner()
    async def delete(self, ctx, member: discord.Member = None):
        try:
            if member is None:
                await errorEmbed.send(ctx, "You must explicitly specify a member!", False)
                return

            result = db.delete_trader(member.id)

            embed = discord.Embed(color=EMBED_COLOR)

            if result:
                embed.set_thumbnail(url=member.avatar)
                embed.title = f"Banished!"
                embed.description = "Deleted the specified trader."

                await ctx.reply(embed=embed)
            else:
                embed.title = "Couldn't find trader!"
                embed.description = f'Did {member.mention} run `{PREFIX}create`?'
                embed.set_thumbnail(url=LOGO)

                await ctx.reply(embed=embed)


        except Exception as e:
            await errorEmbed.send(ctx, e)
    
    @commands.command()
    @commands.check(_moderation_access)
    async def reset(self, ctx, member: discord.Member = None, grade_type: str = None):
        try:
            if member is None or grade_type is None:
                await errorEmbed.send(ctx, f"Incorrect usage!\n\nTypes:\nlow\nmedium\nhigh\nall\n\nEx.\n{PREFIX}reset <member> <grade>", False)
                return
            
            grade_type = grade_type.lower()
            
            if grade_type == 'all':
                result = db.reset_trader_all_balances(member.id)
            elif grade_type == 'high':
                result = db.reset_trader_grade_balance(member.id, 'high_grade_balance')
            elif grade_type == 'medium':
                result = db.reset_trader_grade_balance(member.id, 'medium_grade_balance')
            elif grade_type == 'low':
                result = db.reset_trader_grade_balance(member.id, 'low_grade_balance')
            else:
                await errorEmbed.send(ctx, "Invalid grade type!\n\nTypes:\nlow\nmedium\nhigh\nall", False)
                return
            
            if not result:
                await errorEmbed.send(ctx, f"There was an error.\n\n{result}", False)
                return
            
            embed: discord.Embed = discord.Embed(
                title='Oh no! All gone, trader...',
                description=f"Reset {grade_type} grade balance(s).",
                color=EMBED_COLOR
            )

            await ctx.reply(embed=embed)

        except Exception as e:
            await errorEmbed.send(ctx, e)


async def setup(bot):
    await bot.add_cog(EconomyModeration(bot))
