import os
import uuid
import json
import discord
from discord.ext import commands
from discord_slash import SlashCommand
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import Counter

DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
GOOGLE_SHEET = os.environ['GOOGLE_SHEET']

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('google-credentials.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
sheet = client.open(GOOGLE_SHEET).sheet1

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix= '!', intents=intents)

@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.command()
async def teamkill(ctx, teamkiller: discord.Member, teamkilled: discord.Member):
    """
    Allow a user to add a teamkill entry to the database
    Format: !teamkill @teamkiller @teamkilled
    """
    await ctx.channel.purge(limit=1)
    await ctx.send(f'{teamkiller.mention} teamkilled {teamkilled.mention}')
    row = [str(uuid.uuid4()),str(teamkiller.id),str(teamkilled.id)]
    sheet.insert_row(row,2)

@bot.command()
async def wallofshame(ctx):
    """
    Display a list of all teamkillers and the number of teamkills
    """
    await ctx.channel.purge(limit=1)
    records = sheet.get_all_records()
    
    stats = dict(Counter(record['teamkiller'] for record in records))

    for key in stats:
        user = bot.get_user(id=int(key))
        kills = stats[key]

        await ctx.send(f'{user.name} has {kills} teamkill(s)')

bot.run(DISCORD_TOKEN)