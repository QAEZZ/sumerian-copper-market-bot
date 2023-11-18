import os
import time
import discord
from constants import EMBED_COLOR
import helpers.errorEmbed as errorEmbed


def _cog_checker(cog: str) -> list:
    if cog[:5].lower() == 'cogs.': cog = cog[5:]

    try:
        cog_folder, cog_name = cog.split('.')
    except ValueError:
        cog_folder, cog_name = [False, False]

    return [cog, cog_folder, cog_name]


class CogHelper:

    def __init__(self, client, ctx):
        self.client = client
        self.ctx = ctx

    async def load(self, cog: str) -> None:
        # cog ex: cogs.core.help
        # cog ex: cogs.core.all

        cog, cog_folder, cog_name = _cog_checker(cog)
        if not cog_name:
            await errorEmbed.send(
                    ctx=self.ctx,
                    e='Please properly format your cog.\n\nEx.\ncogs.core.help'
            )
            return

        embed: discord.Embed = discord.Embed(
                title="Result", color=EMBED_COLOR
        )

        msg = await self.ctx.reply(embed=embed)

        if cog_name == 'all':
            for filename in os.listdir(f"cogs/{cog_folder}"):
                if filename.endswith('.py'):
                    try:
                        cog = f'cogs.{cog_folder}.{filename[:-3]}'
                        await self.client.load_extension(cog)
                        embed.add_field(
                                name='✅',
                                value=f'```{cog} loaded.```',
                                inline=False
                        )
                    except Exception as e:
                        embed.add_field(name='❌', value=f'```{e}```', inline=False)

                    time.sleep(.75) # ratelimit
                    await msg.edit(embed=embed)

            embed.set_footer(text='All done 👍')
            await msg.edit(embed=embed)
            return
        
        try:
            await self.client.load_extension(f'cogs.{cog}')
            embed.add_field(name='✅', value=f'```cogs.{cog} loaded.```')
        except Exception as e:
            embed.add_field(name='❌', value=f'```\n{e}\n```')

        await msg.edit(embed=embed)


    async def unload(self, cog: str) -> None:
        cog, cog_folder, cog_name = _cog_checker(cog)
        if not cog_name:
            await errorEmbed.send(
                    ctx=self.ctx,
                    e='Please properly format your cog.\n\nEx.\ncogs.core.help'
            )
            return

        embed: discord.Embed = discord.Embed(
                title="Result", color=EMBED_COLOR
        )

        msg = await self.ctx.reply(embed=embed)

        if cog_name == 'all':
            for filename in os.listdir(f'cogs/{cog_folder}'):
                if filename.endswith('.py'):
                    try:
                        cog = f'cogs.{cog_folder}.{filename[:-3]}'
                        await self.client.unload_extension(cog)
                        embed.add_field(
                                name='✅',
                                value=f'```{cog} unloaded.```',
                                inline=False
                        )
                    except Exception as e:
                        embed.add_field(name='❌', value=f'```{e}```', inline=False)

                    time.sleep(.75) # ratelimit
                    await msg.edit(embed=embed)

            embed.set_footer(text='All done 👍')
            await msg.edit(embed=embed)
            return

        try:
            await self.client.unload_extension(f'cogs.{cog}')
            embed.add_field(name='✅', value=f'```cogs.{cog} unloaded.```')
        except Exception as e:
            embed.add_field(name='❌', value=f'```\n{e}\n```')

        await msg.edit(embed=embed)


    async def reload(self, cog: str) -> None:
        cog, cog_folder, cog_name = _cog_checker(cog)
        if not cog_name:
            await errorEmbed.send(
                    ctx=self.ctx,
                    e='Please properly format your cog.\n\nEx.\ncogs.core.help'
            )
            return

        embed: discord.Embed = discord.Embed(
                title='Result', color=EMBED_COLOR
        )

        msg = await self.ctx.reply(embed=embed)

        if cog_name == 'all':
            for filename in os.listdir(f'cogs/{cog_folder}'):
                if filename.endswith('.py'):
                    try:
                        cog = f'cogs.{cog_folder}.{filename[:-3]}'
                        await self.client.unload_extension(cog)
                        await self.client.load_extension(cog)
                        embed.add_field(
                                name='✅',
                                value=f'```{cog} reloaded.```',
                                inline=False
                        )
                    except Exception as e:
                        embed.add_field(name='❌', value=f'```{e}```', inline=False)

                    time.sleep(.75) # ratelimit
                    await msg.edit(embed=embed)

            embed.set_footer(text='All done 👍')
            await msg.edit(embed=embed)
            return

        try:
            await self.client.unload_extension(f'cogs.{cog}')
            await self.client.load_extension(f'cogs.{cog}')
            embed.add_field(name='✅', value=f'```cogs.{cog} reloaded.```')
        except Exception as e:
            embed.add_field(name='❌', value=f'```\n{e}\n```')

        await msg.edit(embed=embed)

