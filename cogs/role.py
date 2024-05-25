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
from discord_slash.utils.manage_commands import create_option

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class Role(commands.Cog, name="role"):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="role",
        description="Give yourself a role",
        options=[
            create_option(
                name="role",
                description="The role you would like to have.",
                option_type=8,
                required=True
            )
        ],
    )
    async def role(self, context: SlashContext, role: discord.Role):
        with open("blacklist.json") as file:
            blacklist = json.load(file)
        if context.author.id in blacklist["ids"]:
            return

        await context.author.add_roles(role, reason="/role")
        await context.send(f"Gave {context.author} the {role} role")

    @cog_ext.cog_slash(
        name="remove",
        description="Remove a role",
        options=[
            create_option(
                name="role",
                description="The role you would like to remove.",
                option_type=8,
                required=True
            )
        ],
    )
    async def remove(self, context: SlashContext, role: discord.Role):
        with open("blacklist.json") as file:
            blacklist = json.load(file)
        if context.author.id in blacklist["ids"]:
            return

        await context.author.remove_roles(role, reason="/role")
        await context.send(f"Took away the {role} role from {context.author}")

def setup(bot):
    bot.add_cog(Role(bot))
