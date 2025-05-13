from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import helper.events
from bot_instance import bot

load_dotenv(dotenv_path=".env")
token = os.getenv("bot_token")

bot.run(token)