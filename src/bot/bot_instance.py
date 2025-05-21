import discord
from discord.ext import commands

# Configure intents to enable relevant event subscriptions
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content (e.g. for on_message)
intents.guilds = True           # Required to access guild-related events and data
intents.members = True          # Required to access member join/leave and role events

# Initialize the bot instance with a command prefix and specified intents
bot = commands.Bot(command_prefix="!", intents=intents)
