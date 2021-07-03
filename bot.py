import os
import uuid
import discord
from discord.ext import commands
from discord_slash import SlashCommand
import gspread
from oauth2client.service_account import ServiceAccountCredentials


DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Trotsky Development").sheet1

bot = commands.Bot(command_prefix= '!')

@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.command()
async def teamkill(ctx, teamkiller: discord.Member, teamkilled: discord.Member):
    await ctx.send(f'{teamkiller.mention} teamkilled {teamkilled.mention}')
    row = [str(uuid.uuid4()),teamkiller.id,teamkilled.id]
    sheet.insert_row(row,2)

bot.run(DISCORD_TOKEN)