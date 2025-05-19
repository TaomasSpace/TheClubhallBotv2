from dotenv import load_dotenv
import os
import discord
from discord import app_commands
from bot_instance import bot
import helper.events
from Commands.boosterPearks import setBoostLevel, customRole, grantrole
from Commands.funCommands import (
    stab,
    punch,
    goon,
    dance,
    good,
    giveaway,
    imitate,
    forceLowerCase,
    fakeBan,
)
from Commands.gameCommands.adminCommands import addMoney, removeMoney, addServerMoney
from Commands.gameCommands.manageMoney import request, donate, balance

load_dotenv(dotenv_path=".env")
token = os.getenv("bot_token")


@bot.tree.command(
    name="setboostlevel", description="Set custom boost level manually (Admin only)"
)
@app_commands.describe(user="User", level="Boost level (1, 2, or 3)")
async def setboostlevelCommand(
    interaction: discord.Interaction, user: discord.Member, level: int
):
    await setBoostLevel.setboostlevel(interaction=interaction, user=user, level=level)


@bot.tree.command(name="customrole", description="Create or update your booster role")
@app_commands.describe(name="Name of your role", color="Hex color like #FFAA00")
async def customroleCommand(interaction: discord.Interaction, name: str, color: str):
    await customRole.customrole(interaction=interaction, name=name, color=color)


@bot.tree.command(
    name="grantrole",
    description="Give your custom role to another user (Boost-Level 2 required)",
)
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


@bot.tree.command(
    name="imitate", description="Imitate a user's message (Admin/Owner only)"
)
@app_commands.describe(user="User to imitate", msg="The message to send")
async def imitateCommand(
    interaction: discord.Interaction, user: discord.Member, msg: str
):
    await imitate.imitate(interaction=interaction, user=user, msg=msg)


@bot.tree.command(
    name="forcelowercase", description="Force a member's messages to lowercase (toggle)"
)
@app_commands.describe(member="Member to lock/unlock")
@app_commands.checks.has_permissions(manage_messages=True)
async def forcelowercaseCommand(
    interaction: discord.Interaction, member: discord.Member
):
    await forceLowerCase.forcelowercase(interaction=interaction, member=member)


@bot.tree.command(
    name="fakeban", description="Create a fake ban message to confuse the members"
)
@app_commands.describe()
async def fakeBanCommand(
    interaction: discord.Interaction, user: discord.Member, reason: str
):
    await fakeBan.fakeBan(interaction=interaction, user=user, reason=reason)


@bot.tree.command(
    name="addmoney", description="Give coins to a user (Admin/Owner only)"
)
async def addMoneyCommand(
    interaction: discord.Interaction, user: discord.Member, amount: int
):
    await addMoney.addMoney(interaction=interaction, user=user, amount=amount)


@bot.tree.command(
    name="remove", description="Remove clubhall coins from a user (Admin/Owner only)"
)
async def removeCommand(
    interaction: discord.Interaction, user: discord.Member, amount: int
):
    await removeMoney.remove(interaction=interaction, user=user, amount=amount)


@bot.tree.command(
    name="balance", description="Check someone else's clubhall coin balance"
)
async def balanceCommand(interaction: discord.Interaction, user: discord.Member):
    await balance.balance(interaction=interaction, user=user)


@bot.tree.command(
    name="request", description="Request clubhall coins from another user"
)
async def requestCommand(
    interaction: discord.Interaction, user: discord.Member, amount: int, reason: str
):
    await request.request(
        interaction=interaction, user=user, amount=amount, reason=reason
    )


@bot.tree.command(name="donate", description="Send coins to another user")
async def donateCommand(
    interaction: discord.Interaction, user: discord.Member, amount: int
):
    await donate.donate(interaction=interaction, user=user, amount=amount)


@bot.tree.command(name="addservermoney", description="add money to the server/bank")
async def addServerMoneyCommand(interaction: discord.Interaction, amount: int):
    await addServerMoney.addServerMoney(interaction=interaction, amount=amount)


bot.run(token)
