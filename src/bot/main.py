from dotenv import load_dotenv
import os
import discord
from discord import app_commands
from bot_instance import bot
import helper.events
from Commands.boosterPearks import setBoostLevel, customRole, grantrole
from Commands.funCommands import stab, punch, goon, dance, good, giveaway, imitate, forceLowerCase

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

@bot.tree.command(name="grantrole", description="Give your custom role to another user (Boost-Level 2 required)",)
@app_commands.describe(target="User to give your custom role to")
async def grantroleCommand(interaction: discord.Interaction, target: discord.Member):
    await grantrole.grantrole(interaction=interaction, target=target)

@bot.tree.command(name="stab", description="Stab someone with anime style")
async def stabCommand(interaction: discord.Interaction, user: discord.Member):
    await stab.stab(interaction=interaction, user=user)

@bot.tree.command(name="punch", description="Punch someone with anime style")
async def punchCommand(interaction: discord.Interaction, user: discord.Member):
    await punch.punch(interaction=interaction, user=user)

@bot.tree.command(name="goon", description="goon to someone on the server")
async def goonCommand(interaction: discord.Interaction, user: discord.Member):
    await goon.goon(interaction=interaction, user=user)

@bot.tree.command(name="dance", description="hit a cool dance")
async def danceCommand(interaction: discord.Interaction):
    await dance.dance(interaction=interaction)

@bot.tree.command(name="good", description="Tell someone he/she is a good boy/girl")
async def goodCommand(interaction: discord.Interaction, user: discord.Member):
    await good.good(interaction=interaction, user=user)

@bot.tree.command(name="giveaway", description="Start a giveaway (only Admin/Owner)")
@app_commands.describe(duration="duration in minutes", prize="Prize")
async def giveawayCommand(interaction: discord.Interaction, duration: int, prize: str):
    await giveaway.giveaway(interaction=interaction, duration=duration, prize=prize)

@bot.tree.command(name="imitate", description="Imitate a user's message (Admin/Owner only)")
@app_commands.describe(user="User to imitate", msg="The message to send")
async def imitateCommand(interaction: discord.Interaction, user: discord.Member, msg: str):
    await imitate.imitate(interaction=interaction, user=user, msg=msg)

@bot.tree.command(name="forcelowercase", description="Force a member's messages to lowercase (toggle)")
@app_commands.describe(member="Member to lock/unlock")
@app_commands.checks.has_permissions(manage_messages=True)
async def forcelowercaseCommand(interaction: discord.Interaction, member: discord.Member):
    await forceLowerCase.forcelowercase(interaction=interaction, member=member)

bot.run(token)