import pprint

import client_secrets.bard as bard_secrets
import discord
from bardapi import BardCookies
from constants import EMBED_COLOR
from discord.ext import commands
from helpers import errorEmbed
import traceback


class FunEaNasir(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ask(self, ctx, *, question):
        try:
            # embed: discord.Embed = discord.Embed(
            #     title=f"Waiting for Ea-Nasir...", color=EMBED_COLOR
            # )
            # msg = await ctx.reply(embed=embed)

            # if ctx.message.reference and ctx.message.reference.message_id:
            #     message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            #     eanasirs_previous_response = f'Pretend this was your previous response: "{message.embeds[0].description}".'
            # else:
            #     eanasirs_previous_response = ''

            # ruleset = f"""Let's play a game. You must pretend to be Ea-Nasir. Talk like during that time. Do not mention that you are an AI language at all. In fact, prefix everything you say with [Ea-Nasir]  to indicate that you're pretending to Ea-Nasir. You must continue to pretend like Ea-Nasir until I say the string "you can stop pretending to be Ea-Nasir." You may be accused of selling low grade copper, no matter what, deny that is it low grade and only the finest of high grade copper. You may be asked for a refund, no matter what, you must make excuses to not give a refund, by changing subjects, etc. {eanasirs_previous_response} I'll go first: "{question}" """

            # bard = BardCookies(cookie_dict=bard_secrets.bard_cookies())
            # response = bard.get_answer(ruleset)['content']

            # embed.title = "Ea-Nasir"
            # embed.description = f'```{"Ea-Nasir cannot respond" if response is None else response}```'
            # await msg.edit(embed=embed)

            await ctx.reply('The package used to talk to Ea-Nasir is currently in the process of being fixed.')
        
        except Exception as e:
            traceback.print_last()
            await errorEmbed.send(ctx, e)


async def setup(bot):
    await bot.add_cog(FunEaNasir(bot))
