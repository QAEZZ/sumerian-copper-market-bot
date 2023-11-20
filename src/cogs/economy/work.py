import random
from math import floor

import discord
from constants import EMBED_COLOR, LOGO, PREFIX
from discord.ext import commands
from helpers import db, errorEmbed

GAMBLE_THRESHOLDS = {"low": 60, "medium": 55, "high": 40}

def generate_weighted_numbers(
    low_grade_weight: float = 0.65,
    medium_grade_weight: float = 0.75,
    high_grade_weight: float = 0.85,
) -> list[int, int, int]:
    return [
        random.choices(
            list(range(20, 151)),
            weights=[low_grade_weight if i <= 87 else 0.35 for i in range(20, 151)],
        )[0],
        random.choices(
            list(range(10, 101)),
            weights=[medium_grade_weight if i <= 58 else 0.25 for i in range(10, 101)],
        )[0],
        random.choices(
            list(range(51)),
            weights=[high_grade_weight if i <= 21 else 0.15 for i in range(51)],
        )[0],
    ]


def create_basic_embed(
    title: str = "", description: str = "", thumbnail_url: str = LOGO
) -> discord.Embed:
    embed = discord.Embed(color=EMBED_COLOR)
    embed.set_thumbnail(url=thumbnail_url)
    embed.title = title
    embed.description = description
    return embed


class EconomyWork(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _process_work_command(
        self, ctx, title: str, low_grade: int, medium_grade: int, high_grade: int
    ) -> None:
        try:
            result = db.get_trader(ctx.author.id)
            embed = create_basic_embed()

            if result:
                embed.set_thumbnail(url=ctx.author.avatar)
                embed.title = title

                embed.add_field(
                    name="Low Grade", value=f"```{low_grade}```", inline=False
                )
                embed.add_field(
                    name="Medium Grade", value=f"```{medium_grade}```", inline=False
                )
                embed.add_field(
                    name="High Grade", value=f"```{high_grade}```", inline=False
                )

                await ctx.reply(embed=embed)

                new_low_grade_balance = result.low_grade_balance + low_grade
                new_medium_grade_balance = result.medium_grade_balance + medium_grade
                new_high_grade_balance = result.high_grade_balance + high_grade

                update_result = db.update_trader(
                    user_id=ctx.author.id,
                    low_grade_balance=new_low_grade_balance,
                    medium_grade_balance=new_medium_grade_balance,
                    high_grade_balance=new_high_grade_balance,
                )

                if update_result is not True:
                    embed.add_field(
                        name="Error!",
                        value="Failed to update balances in the database!",
                        inline=False,
                    )
                    embed.set_thumbnail(url=LOGO)
                    ctx.command.reset_cooldown(ctx)
            else:
                embed.title = "Couldn't find trader!"
                embed.description = f"Did you run `{PREFIX}create`?"
                embed.set_thumbnail(url=LOGO)

                await ctx.reply(embed=embed)
                ctx.command.reset_cooldown(ctx)

        except Exception as e:
            await errorEmbed.send(ctx, e)

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def beg(self, ctx):
        try:
            low_grade, medium_grade, high_grade = generate_weighted_numbers(1, 1, 1)

            low_grade = floor(low_grade / 2)
            medium_grade = floor(medium_grade / 4)
            high_grade = 0

            await self._process_work_command(
                ctx,
                "A kind soul has given you the following:",
                low_grade,
                medium_grade,
                high_grade,
            )
        except Exception as e:
            await errorEmbed.send(ctx, e)

    @commands.command()
    @commands.cooldown(1, 7200, commands.BucketType.user)
    async def mine(self, ctx):
        try:
            low_grade, medium_grade, high_grade = generate_weighted_numbers()
            await self._process_work_command(
                ctx, "This is your haul from mining:", low_grade, medium_grade, high_grade
            )
        except Exception as e:
            await errorEmbed.send(ctx, e)

    @commands.command()
    async def gamble(self, ctx, amount_to_gamble: int, what_to_gamble: str):
        try:
            gamble_types = ["low", "medium", "high"]

            if (
                what_to_gamble.lower() not in gamble_types
                or what_to_gamble is None
                or amount_to_gamble is None
            ):
                await errorEmbed.send(
                    ctx,
                    "Invalid gamble type. Please choose 'low', 'medium', or 'high'.\n\nEx.\ncsm.gamble 10 low\ncsm.gamble <amount> <type>",
                )
                return

            result = db.get_trader(user_id=ctx.author.id)

            if not result:
                await errorEmbed.send(
                    ctx,
                    f"Couldn't find your trader information. Have you ran `{PREFIX}create`?",
                    False,
                )
                return

            grade_balance = getattr(result, f"{what_to_gamble}_grade_balance", 0)

            if amount_to_gamble > grade_balance:
                await errorEmbed.send(
                    ctx,
                    f"You don't have enough {what_to_gamble}-grade balance to gamble that amount.",
                    False,
                )
                return

            gamble_result = random.randint(1, 100)
            threshold = GAMBLE_THRESHOLDS.get(what_to_gamble, 50)

            embed = create_basic_embed()
            embed.title = (
                "MY FELLOW MESOPOTAMIAN, YOU WON!"
                if gamble_result > threshold
                else "You lost, boohoo. Go sell your low-grade copper at high-grade price."
            )
            change_in_balance = amount_to_gamble * (
                2 if gamble_result > threshold else -1
            )
            embed.description = f"You {'gained' if gamble_result > threshold else 'lost'} `{change_in_balance}` in {what_to_gamble}-grade balance."

            update_result = db.execute_raw_sql(
                f"UPDATE traders SET {what_to_gamble}_grade_balance = {what_to_gamble}_grade_balance + {change_in_balance} WHERE user_id={ctx.author.id}"
            )

            await ctx.reply(embed=embed)

            if update_result is not True:
                await errorEmbed.send(
                    ctx,
                    f"There was an error updating your balance.\n\n{update_result}",
                    False,
                )

        except Exception as e:
            await errorEmbed.send(ctx, e)

    @commands.command()
    async def rps(self, ctx, choice: str = None, grade: str = None, bet: int = 0):
        valid_choices = ["rock", "paper", "scissors"]

        if choice is None or choice.lower() not in valid_choices:
            await errorEmbed.send(ctx, f"Incorrect usage!\n\nEx.\n{PREFIX}rps <choice> [grade] [amount]", False)
            return

        choice = choice.lower()
        user_choice_index = valid_choices.index(choice)

        computer_choice_index = random.randint(0, 2)

        while hasattr(self, "last_computer_choice") and computer_choice_index == self.last_computer_choice:
            computer_choice_index = random.randint(0, 2)

        self.last_computer_choice = computer_choice_index

        embed: discord.Embed = create_basic_embed(description=f"Ea-Nasir picked `{valid_choices[computer_choice_index]}`, you picked `{choice}`.")

        if user_choice_index == computer_choice_index:
            embed.title = "It's a tie!"
            embed.description = "You have tied with Ea-Nasir."
            await ctx.reply(embed=embed)
            return

        elif (user_choice_index == 0 and computer_choice_index == 2) or \
            (user_choice_index == 1 and computer_choice_index == 0) or \
            (user_choice_index == 2 and computer_choice_index == 1):
            embed.title = "You won, Trader!"
        else:
            embed.title = "Ea-Nasir snatched your copper!"
            bet = bet * -1

        if grade is None and bet is None:
            await ctx.reply(embed=embed)
            return

        elif grade not in ["low", "medium", "high"]:
            await errorEmbed.send(ctx, f"Incorrect usage!\n\nEx.\n{PREFIX}rps <choice> [grade] [amount]", False)
            return

        result = db.get_trader(ctx.author.id)

        if not result:
            await errorEmbed.send(ctx, f"Couldn't find your trader information. Have you run `{PREFIX}create`?", False)

        elif bet > int(getattr(result, f"{grade}_grade_balance", 0)):
            await errorEmbed.send(ctx, f'You do not have enough {grade} balance.\nYou have {getattr(result, f"{grade}_grade_balance", 0)} grade balance.', False)
            return

        update_result = db.execute_raw_sql(f"UPDATE traders SET {grade}_grade_balance = {grade}_grade_balance + {bet} WHERE user_id={ctx.author.id}")

        await ctx.reply(embed=embed)

        if update_result is not True:
            await errorEmbed.send(ctx, f"There was an error updating your balance.\n\n{update_result}", False)




async def setup(bot):
    await bot.add_cog(EconomyWork(bot))
