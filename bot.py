import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand

DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

client = commands.Bot(command_prefix= '!')

@client.event
async def on_ready():
    print('Bot is ready.')

@client.command()
async def teamkill(ctx, teamkiller: discord.Member, teamkilled: discord.Member):
    await ctx.send(f'{teamkiller.mention} teamkilled {teamkilled.mention}')

client.run(DISCORD_TOKEN)