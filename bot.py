import os
import discord
from discord.ext import commands

DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

client = commands.Bot(command_prefix= '/')

@client.event
async def on_ready():
    print('Bot is ready.')

client.run(DISCORD_TOKEN)