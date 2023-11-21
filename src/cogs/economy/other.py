import random
from math import floor

import discord
from constants import EMBED_COLOR, LOGO, PREFIX
from discord.ext import commands
from helpers import db, errorEmbed

from econ_types.trader import Trader

CONVERSIONS = {"low": 15, "medium": 5, "high": 1}


def create_basic_embed(
    title: str = "", description: str = "", thumbnail_url: str = LOGO
) -> discord.Embed:
    embed = discord.Embed(color=EMBED_COLOR)
    embed.set_thumbnail(url=thumbnail_url)
    embed.title = title
    embed.description = description
    return embed


class EconomyOther(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def convert(self, ctx, convert_amount = None, convert_from: str = None, convert_to: str = None):
        try:
            convert_types = ['low', 'medium', 'high']

            if convert_amount is None \
            or convert_from not in convert_types \
            or convert_to not in convert_types:
                await errorEmbed.send(
                    ctx, f'Incorrect Usage!\n\nTypes:\nlow\nmedium\nhigh\n\nEx.\n{PREFIX}convert <amount> <from> <to>\n\nConversion:\n15 low = 5 medium = 1 high', False)
                return
            
            result = db.get_trader(ctx.author.id)
            convert_amount = int(convert_amount.replace(',', ''))

            if not isinstance(result, Trader):
                await errorEmbed.send(ctx, f"Did you run `{PREFIX}create`?", False)
                return
            
            elif convert_amount > getattr(result, f'{convert_from}_grade_balance', 0):
                await errorEmbed.send(ctx, f"You do not that much {convert_from}-grade balance!", False)
                return
            embed: discord.Embed = create_basic_embed('Loading...')
            msg = await ctx.reply(embed=embed)
            

            conversion_rate = CONVERSIONS[convert_to] / CONVERSIONS[convert_from]
            converted_amount = round(convert_amount * conversion_rate)


            setattr(result, f'{convert_from}_grade_balance', getattr(result, f'{convert_from}_grade_balance') - convert_amount)
            setattr(result, f'{convert_to}_grade_balance', getattr(result, f'{convert_to}_grade_balance') + converted_amount)


            update_result = db.update_trader(ctx.author.id,
                                             low_grade_balance=result.low_grade_balance,
                                             medium_grade_balance=result.medium_grade_balance,
                                             high_grade_balance=result.high_grade_balance)
            
            if update_result is not True:
                await errorEmbed.send(ctx, f"Error updating the database: {e}", False)   
                return
                
            embed.title = 'Converted!'
            embed.description = f'Successfully converted `{convert_amount:,}` {convert_from}-grade to `{converted_amount:,}` {convert_to}-grade.'
            embed.set_footer(text='rounded to the nearest whole number')
                
            await msg.edit(embed=embed)
        
        except Exception as e:
            await errorEmbed.send(ctx, e)
  





async def setup(bot):
    await bot.add_cog(EconomyOther(bot))
