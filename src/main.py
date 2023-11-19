#!/usr/bin/env python3

import constants
import asyncio
import os, sys

import tests.run_tests as tester
import datetime

import discord
from discord.ext import commands

from colorama import init, Fore, Style, Back

from helpers import cogs


class TerryClient(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=constants.PREFIX,
            help_command=None,
            intents=discord.Intents.all(),
            activity=constants.ACTIVITY,
        )
        init(autoreset=True)

    async def on_ready(self):
        children = [os.path.join("cogs", child) for child in os.listdir("cogs")]
        cog_folders = filter(os.path.isdir, children)
        for folder in cog_folders:
            for filename in os.listdir(folder):
                if filename.endswith(".py"):
                    try:
                        dir = folder.replace("cogs/", "")
                        print(
                            f"{Style.BRIGHT}{Back.BLUE}{Fore.BLACK}[ INFO    ]{Style.RESET_ALL}{Style.BRIGHT} :: {Style.RESET_ALL}found cogs.{dir}.{filename}"
                        )
                        await client.load_extension(f"cogs.{dir}.{filename[:-3]}")
                        print(
                            f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}[ SUCCESS ]{Style.RESET_ALL}{Style.BRIGHT} :: {Style.RESET_ALL}loaded cogs.{dir}.{filename}"
                        )
                    except Exception as e:
                        print(
                            f"{Style.BRIGHT}{Back.RED}{Fore.BLACK}[ ERROR   ]{Style.RESET_ALL}{Style.BRIGHT} :: {Style.RESET_ALL}{e}"
                        )

        print(
            f"\n\nlogged in as {self.user}\nI am in {len(client.guilds)} server(s)!\n\ndiscord.py == {discord.__version__}\npython == {sys.version}\n\n"
        )


client = TerryClient()


def _cog_access(ctx):
    if ctx.author.id in constants.COG_ACCESS:
        return True
    return False


@client.command()
@commands.check(_cog_access)
async def allowed(ctx):
    await ctx.reply("You're allowed.")


@client.command()
@commands.check(_cog_access)
async def load(ctx, cog: str):
    cog_helper = cogs.CogHelper(client, ctx)
    await cog_helper.load(cog)


@client.command()
@commands.check(_cog_access)
async def unload(ctx, cog: str):
    cog_helper = cogs.CogHelper(client, ctx)
    await cog_helper.unload(cog)


@client.command()
@commands.check(_cog_access)
async def reload(ctx, cog: str):
    cog_helper = cogs.CogHelper(client, ctx)
    await cog_helper.reload(cog)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        retry_after = datetime.datetime.utcnow() + datetime.timedelta(seconds=error.retry_after)
        timestamp = int(retry_after.replace(tzinfo=datetime.timezone.utc).timestamp())
        formatted_time = f"<t:{timestamp}:R>"

        embed = discord.Embed(
            title="Slow down, Trader!",
            description=f"Try again {formatted_time}",
            color=discord.Color.from_rgb(255, 100, 100),
        )
        await ctx.reply(embed=embed)


def setup():
    tester.start()
    asyncio.run(start_client())

async def start_client():
    with open(os.path.abspath("secrets/token.key"), "r") as f:
        TOKEN = f.read()

        await client.start(TOKEN)


if __name__ == "__main__":
    setup()
