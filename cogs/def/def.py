import json
import os
import sys

import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from helpers import json_manager

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

#Change DEFAULT to name of file
class DEFAULT(commands.Cog, name="DEFAULT"):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="test",
        description="test",
    )
    async def test(self, context: SlashContext):
        # This is, for now, only temporary
        with open("blacklist.json") as file:
            blacklist = json.load(file)
        if context.author.id in blacklist["ids"]:
            return

        embed = discord.Embed(
            description="You used /test!",
            color=0x42F56C
        )
        await context.send(embed=embed)

    @commands.command(name="test")
    async def test(self, context):
        # This is, for now, only temporary
        with open("blacklist.json") as file:
            blacklist = json.load(file)
        if context.author.id in blacklist["ids"]:
            return

        embed = discord.Embed(
            title="Error!",
            description="You used r.test!",
            color=0xE02B2B
        )
        await context.send(embed=embed)

def setup(bot):
    bot.add_cog(owner(bot))
