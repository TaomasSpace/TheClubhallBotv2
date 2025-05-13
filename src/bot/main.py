from dotenv import load_dotenv
import os
import discord
from discord import app_commands
from bot_instance import bot
import helper.events
from Commands.boosterPearks import setBoostLevel, customRole
from 

load_dotenv(dotenv_path=".env")
token = os.getenv("bot_token")

@bot.tree.command(name="setboostlevel", description="Set custom boost level manually (Admin only)")
@app_commands.describe(user="User", level="Boost level (1, 2, or 3)")
async def setboostlevelCommand(interaction: discord.Interaction, user: discord.Member, level: int):
    await setBoostLevel.setboostlevel(interaction=interaction, user=user, level=level)

@bot.tree.command(name="customrole", description="Create or update your booster role")
@app_commands.describe(name="Name of your role", color="Hex color like #FFAA00")
async def customroleCommand(interaction: discord.Interaction, name: str, color: str):
    await customRole.customrole(interaction=interaction, name=name, color=color)

bot.run(token)