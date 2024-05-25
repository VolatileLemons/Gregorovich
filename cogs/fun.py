""""
Copyright © Krypton 2021 - https://github.com/kkrypt0nn
Description:
This is a template to create your own discord bot in python.

Version: 3.0
"""

import json
import os
import sys
import random

import aiohttp
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="randomfact",
        description="Get a random fact."
    )
    async def randomfact(self, context: SlashContext):
        """
        Get a random fact.
        """

        # This is, for now, only temporary
        with open("blacklist.json") as file:
            blacklist = json.load(file)
        if context.author.id in blacklist["ids"]:
            return

        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(description=data["text"], color=0xD75BF4)
                    await context.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                    await context.send(embed=embed)

    @cog_ext.cog_slash(
        name="roll",
        description="Roll a D20",
        options=[
        ],
    )
    async def roll(self, context: SlashContext):
        """
        Roll a D20
        """

        # This is, for now, only temporary
        with open("blacklist.json") as file:
            blacklist = json.load(file)
        if context.author.id in blacklist["ids"]:
            return

        answers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
        embed = discord.Embed(
            title="You rolled a",
            description=f"{answers[random.randint(0, len(answers))]}",
            color=0x42F56C
        )
        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
