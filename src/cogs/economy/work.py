import discord
from discord.ext import commands
from constants import EMBED_COLOR, PREFIX, LOGO
from helpers import errorEmbed
from econ_types.trader import Trader, db_create_trader

import sqlite3
import random


def generate_weighted_numbers(weight_1: float = 0.65, weight_2: float = 0.75, weight_3: float = 0.85) -> list[int, int, int]:
    # range 25-150
    int1_choices = list(range(25, 151))
    int1 = random.choices(int1_choices, weights=[weight_1 if i <= 87 else 0.35 for i in int1_choices])[0]

    # 15-100
    int2_choices = list(range(15, 101))
    int2 = random.choices(int2_choices, weights=[weight_2 if i <= 58 else 0.25 for i in int2_choices])[0]

    # range 0-25 
    int3_choices = list(range(26))
    int3 = random.choices(int3_choices, weights=[weight_3 if i <= 21 else 0.15 for i in int3_choices])[0]

    return [int1, int2, int3]


class EconomyWork(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 7200, commands.BucketType.user)
    async def mine(self, ctx):
        try:
            low_grade, medium_grade, high_grade = generate_weighted_numbers()

            conn = sqlite3.connect("db/traders.db")
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM traders WHERE user_id=?", (ctx.author.id,))
            result = cursor.fetchone()

            embed = discord.Embed(color=EMBED_COLOR)

            if result:
                embed.set_thumbnail(url=ctx.author.avatar)
                embed.title = f"This is your haul from mining:"

                embed.add_field(name="Low Grade Earned", value=f'```{low_grade}```', inline=False)
                embed.add_field(name="Med Grade Earned", value=f'```{medium_grade}```', inline=False)
                embed.add_field(name="High Grade Earned", value=f'```{high_grade}```', inline=False)

                await ctx.reply(embed=embed)

                low_grade_balance = result[2] + low_grade
                medium_grade_balance = result[3] + medium_grade
                high_grade_balance = result[4] + high_grade

                cursor.execute("UPDATE traders SET low_grade_balance=?, medium_grade_balance=?, high_grade_balance=? WHERE user_id=?",
                            (low_grade_balance, medium_grade_balance, high_grade_balance, ctx.author.id))

                conn.commit()

            else:
                embed.title = "Couldn't find trader!"
                embed.description = f'Did you run `{PREFIX}create`?'
                embed.set_thumbnail(url=LOGO)

                await ctx.reply(embed=embed)
                ctx.command.reset_cooldown(ctx)
            
            conn.close()

        except Exception as e:
            await errorEmbed.send(ctx, e)
    

    @commands.command()
    async def gamble(self, ctx, what_to_gamble: str, amount_to_gamble: int):
        try:
            gamble_types = ['low', 'medium', 'high']

            if what_to_gamble.lower() not in gamble_types or what_to_gamble is None or amount_to_gamble is None:
                await errorEmbed.send(ctx, "Invalid gamble type. Please choose 'low', 'medium', or 'high'.")
                return

            conn = sqlite3.connect("db/traders.db")
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM traders WHERE user_id=?", (ctx.author.id,))
            result = cursor.fetchone()

            if not result:
                await errorEmbed.send(ctx, f"Couldn't find your trader information. Have you run `{PREFIX}create`?")
                conn.close()
                return

            user_low_balance = result[2]
            user_medium_balance = result[3]
            user_high_balance = result[4]

            if what_to_gamble == 'low' and amount_to_gamble > user_low_balance:
                await errorEmbed.send(ctx, "You don't have enough low-grade balance to gamble that amount.")
                conn.close()
                return
            elif what_to_gamble == 'medium' and amount_to_gamble > user_medium_balance:
                await errorEmbed.send(ctx, "You don't have enough medium-grade balance to gamble that amount.")
                conn.close()
                return
            elif what_to_gamble == 'high' and amount_to_gamble > user_high_balance:
                await errorEmbed.send(ctx, "You don't have enough high-grade balance to gamble that amount.")
                conn.close()
                return

            gamble_result = random.randint(1, 100)

            threshold = 50
            if what_to_gamble == 'low':
                threshold = 65
            elif what_to_gamble == 'medium':
                threshold = 75
            elif what_to_gamble == 'high':
                threshold = 85

            embed: discord.Embed = discord.Embed(color=EMBED_COLOR)
            embed.set_thumbnail(url=LOGO)

            if gamble_result > threshold:
                # Win the gamble
                change_in_balance = amount_to_gamble * 2
                embed.title = "MY FELLOW MESOPOTAMIAN, YOU WON!"
                embed.description = f"You gained `{change_in_balance}` in {what_to_gamble}-grade balance."
                
            else:
                # Lose the gamble
                change_in_balance = amount_to_gamble * -1
                embed.title = "You lost, boohoo. Go sell your low-grade copper at high-grade price."
                embed.description = f"You lost `{change_in_balance}` in {what_to_gamble}-grade balance."
            
            await ctx.reply(embed=embed)

            cursor.execute(f"UPDATE traders SET {what_to_gamble}_grade_balance = {what_to_gamble}_grade_balance + ? WHERE user_id=?", (change_in_balance, ctx.author.id))

            conn.commit()
            conn.close()

        except Exception as e:
            await errorEmbed.send(ctx, e)


async def setup(bot):
    await bot.add_cog(EconomyWork(bot))