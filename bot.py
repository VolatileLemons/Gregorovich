import json
import os
import platform
import random
import sys
import re

from helpers import json_manager

import discord
#1.7.3
from discord.ext import tasks
from discord.ext.commands import Bot
from discord_slash import SlashCommand, SlashContext
#3.0.2  

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)
log = open('messagelog.txt', 'a', encoding="utf-8")

"""	
Setup bot intents (events restrictions)
For more information about intents, please go to the following websites:
https://discordpy.readthedocs.io/en/latest/intents.html
https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents


Default Intents:
intents.messages = True
intents.reactions = True
intents.guilds = True
intents.emojis = True
intents.bans = True
intents.guild_typing = False
intents.typing = False
intents.dm_messages = False
intents.dm_reactions = False
intents.dm_typing = False
intents.guild_messages = True
intents.guild_reactions = True
intents.integrations = True
intents.invites = True
intents.voice_states = False
intents.webhooks = False

Privileged Intents (Needs to be enabled on dev page), please use them only if you need them:
intents.presences = True
intents.members = True
"""

intents = discord.Intents.all()

#intents.voice_states = True
#intents.messages = True

bot = Bot(command_prefix=config["bot_prefix"], intents=intents)
slash = SlashCommand(bot, sync_commands=True)


# The code in this even is executed when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    status_task.start()


# Setup the game status task of the bot
@tasks.loop(minutes=0.10)
async def status_task():
    statuses = ["on the Metaverse", "with your mom", "polonium", "monolith", "in Chairotion", ""]
    #await bot.change_presence(activity=discord.Activity(name="the Metaverse", type=3))
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))

# Removes the default help command of discord.py to be able to create our custom help command.
bot.remove_command("help")

if __name__ == "__main__":
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


# The code in this event is executed every time someone sends a message, with or without the prefix
@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return
    elif re.search("MUD", message.content.upper()) or re.search("KIP", message.content.upper()):
        await message.channel.send("**mudkip**")
    elif message.content == "brrt": 
        await message.channel.send("We shall remember you Murk...")
    elif re.search("LORE", message.content.upper()): 
        await message.channel.send(":notes:You didn't have to cut me off:notes:")
    elif re.search("ENCHANTED", message.content.upper()): 
        await message.channel.send(":notes:I was enchanted to meeet youuuuuuuu!:notes:")
        #print("🍪")
    elif re.search("ALLAN", message.content.upper()): 
        await message.channel.send("You are kenough!")
    await bot.process_commands(message)
    log.write(f"Message: '{message.content}' --- sent by '{message.author.name}' ({message.author.id}) in '{message.channel.name}' ({message.channel.id}) Guild: '{message.guild.name}' ({message.guild.id}) \n")

# The code in this event is executed every time a command has been *successfully* executed
@bot.event
async def on_slash_command(ctx: SlashContext):
    fullCommandName = ctx.name
    split = fullCommandName.split(" ")
    executedCommand = str(split[0])
    #print(
        #f"Executed {executedCommand} command in {ctx.guild.name} (ID: {ctx.guild.id}) by {ctx.author} (ID: {ctx.author.id})")
    log.write(f"Executed {executedCommand} command in {ctx.guild.name} (ID: {ctx.guild.id}) by {ctx.author} (ID: {ctx.author.id}) \n")

@bot.event
async def on_voice_state_update(member, before, after):
    pass

# The code in this event is executed every time a valid commands catches an error
@bot.event
async def on_command_error(context, error):
    raise error

# Run the bot with the token
bot.run(config["token"])
