from dotenv import load_dotenv
import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

load_dotenv(dotenv_path=".env")
token = os.getenv("bot_token")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot is online as {bot.user}")


bot.run(token)