from dotenv import load_dotenv
import os
import discord
from discord import app_commands
from discord.app_commands import cooldown
from bot_instance import bot
import helper.events  # Event handlers are imported here to be registered
from Commands.boosterPearks import customRole, grantrole, imitate
from Commands.funCommands import (
    stab,
    punch,
    goon,
    dance,
    good,
    giveaway,
    forceLowerCase,
    fakeBan,
    addReactionRole,
)
from Commands.gameCommands.adminCommands import (
    addMoney,
    removeMoney,
    addServerMoney,
    setStatpoints,
)
from Commands.gameCommands.manageMoney import request, donate, balance
from Commands.gameCommands.manageStats import stats, allocate, buyPoints
from Commands.gameCommands.userInteractionCommands import hack

# Load token from environment file
load_dotenv(dotenv_path=".env")
token = os.getenv("bot_token")


@bot.tree.command(name="customrole", description="Create or update your booster role")
@app_commands.describe(name="Name of your role", color="Hex color like #FFAA00")
@cooldown(rate=1, per=2.0, key=lambda i: i.user.id)
async def customroleCommand(interaction: discord.Interaction, name: str, color: str):
    await customRole.customrole(interaction=interaction, name=name, color=color)


@bot.tree.command(
    name="grantrole",
    description="Give your custom role to another user",
)
@cooldown(rate=1, per=2.0, key=lambda i: i.user.id)
@app_commands.describe(target="User to give your custom role to")
async def grantroleCommand(interaction: discord.Interaction, target: discord.Member):
    await grantrole.grantrole(interaction=interaction, target=target)


# ───── Fun Commands ─────
@cooldown(rate=1, per=2.0, key=lambda i: i.user.id)
@bot.tree.command(name="stab", description="Stab someone with anime style")
async def stabCommand(interaction: discord.Interaction, user: discord.Member):
    await stab.stab(interaction=interaction, user=user)


@cooldown(rate=1, per=2.0, key=lambda i: i.user.id)
@bot.tree.command(name="punch", description="Punch someone with anime style")
async def punchCommand(interaction: discord.Interaction, user: discord.Member):
    await punch.punch(interaction=interaction, user=user)


@cooldown(rate=1, per=2.0, key=lambda i: i.user.id)
@bot.tree.command(name="goon", description="Goon to someone on the server")
async def goonCommand(interaction: discord.Interaction, user: discord.Member):
    await goon.goon(interaction=interaction, user=user)


@cooldown(rate=1, per=2.0, key=lambda i: i.user.id)
@bot.tree.command(name="dance", description="Hit a cool dance")
async def danceCommand(interaction: discord.Interaction):
    await dance.dance(interaction=interaction)


@cooldown(rate=1, per=2.0, key=lambda i: i.user.id)
@bot.tree.command(name="good", description="Tell someone they are a good boy/girl")
async def goodCommand(interaction: discord.Interaction, user: discord.Member):
    await good.good(interaction=interaction, user=user)


@cooldown(rate=1, per=2.0, key=lambda i: i.user.id)
@bot.tree.command(name="giveaway", description="Start a giveaway (Admin/Owner only)")
@app_commands.describe(duration="Duration in minutes", prize="Prize to be won")
async def giveawayCommand(interaction: discord.Interaction, duration: int, prize: str):
    await giveaway.giveaway(interaction=interaction, duration=duration, prize=prize)


@cooldown(rate=1, per=2.0, key=lambda i: i.user.id)
@bot.tree.command(
    name="imitate", description="Imitate a user's message (Admin/Owner only)"
)
@app_commands.describe(user="User to imitate", msg="Message content")
async def imitateCommand(
    interaction: discord.Interaction, user: discord.Member, msg: str
):
    await imitate.imitate(interaction=interaction, user=user, msg=msg)


@cooldown(rate=1, per=2.0, key=lambda i: i.user.id)
@bot.tree.command(
    name="forcelowercase", description="Force a member's messages to lowercase (toggle)"
)
@app_commands.describe(member="Member to lock/unlock")
@app_commands.checks.has_permissions(manage_messages=True)
async def forcelowercaseCommand(
    interaction: discord.Interaction, member: discord.Member
):
    await forceLowerCase.forcelowercase(interaction=interaction, member=member)


@cooldown(rate=1, per=2.0, key=lambda i: i.user.id)
@bot.tree.command(
    name="fakeban", description="Create a fake ban message to confuse members"
)
async def fakeBanCommand(
    interaction: discord.Interaction, user: discord.Member, reason: str
):
    await fakeBan.fakeBan(interaction=interaction, user=user, reason=reason)


# ───── Coin Management (Admin) ─────
@bot.tree.command(
    name="addmoney", description="Give coins to a user (Admin/Owner only)"
)
async def addMoneyCommand(
    interaction: discord.Interaction, user: discord.Member, amount: int
):
    await addMoney.addMoney(interaction=interaction, user=user, amount=amount)


@bot.tree.command(
    name="remove", description="Remove coins from a user (Admin/Owner only)"
)
async def removeCommand(
    interaction: discord.Interaction, user: discord.Member, amount: int
):
    await removeMoney.remove(interaction=interaction, user=user, amount=amount)


@bot.tree.command(
    name="addservermoney", description="Add coins to the server/bank balance"
)
async def addServerMoneyCommand(interaction: discord.Interaction, amount: int):
    await addServerMoney.addServerMoney(interaction=interaction, amount=amount)


# ───── Coin Management (User) ─────
@cooldown(rate=1, per=2.0, key=lambda i: i.user.id)
@bot.tree.command(name="balance", description="Check someone's coin balance")
async def balanceCommand(interaction: discord.Interaction, user: discord.Member):
    await balance.balance(interaction=interaction, user=user)


@cooldown(rate=1, per=2.0, key=lambda i: i.user.id)
@bot.tree.command(name="request", description="Request coins from another user")
async def requestCommand(
    interaction: discord.Interaction, user: discord.Member, amount: int, reason: str
):
    await request.request(
        interaction=interaction, user=user, amount=amount, reason=reason
    )


@cooldown(rate=1, per=2.0, key=lambda i: i.user.id)
@bot.tree.command(name="donate", description="Send coins to another user")
async def donateCommand(
    interaction: discord.Interaction, user: discord.Member, amount: int
):
    await donate.donate(interaction=interaction, user=user, amount=amount)


@bot.tree.command(name="setstat", description="Set a user's stat (Admin only)")
@app_commands.describe(
    user="Target user",
    stat="Which stat to set ((empty=statPoints), intelligence, strength, stealth, influence, awareness)",
    amount="New stat value (≥ 0)",
)
async def setstatPointsCommand(
    interaction: discord.Interaction,
    user: discord.Member,
    amount: int,
    stat: str | None = None,
):
    await setStatpoints.setstat(
        interaction=interaction, user=user, stat=stat, amount=amount
    )


@cooldown(rate=1, per=2.0, key=lambda i: i.user.id)
@bot.tree.command(name="stats", description="Show your stats & unspent points")
async def statsCommand(
    interaction: discord.Interaction, user: discord.Member | None = None
):
    await stats.stats(interaction=interaction, user=user)


@cooldown(rate=1, per=2.0, key=lambda i: i.user.id)
@bot.tree.command(name="allocate", description="Spend stat‑points to increase a stat")
@app_commands.describe(
    stat="Which stat? (intelligence/strength/stealth/influence/awareness)",
    points="How many points to allocate",
)
async def allocateCommand(interaction: discord.Interaction, stat: str, points: int):
    await allocate.allocate(interaction=interaction, stat=stat, points=points)


@cooldown(rate=1, per=2.0, key=lambda i: i.user.id)
@bot.tree.command(name="buypoints", description="Buy stat‑points with coins")
async def buypointsCommand(interaction: discord.Interaction, amount: int = 1):
    await buyPoints.buypoints(interaction=interaction, amount=amount)


@cooldown(rate=1, per=2400, key=lambda i: i.user.id)
@bot.tree.command(
    name="hack", description="Hack the bank to win coins (needs intelligence ≥ 5)"
)
async def hackCommand(interaction: discord.Interaction):
    await hack.hack(interaction=interaction)


@bot.tree.command(
    name="addcolorreactionrole", description="Add emoji-role to color reaction message"
)
@app_commands.describe(emoji="Emoji to react with", role="Role to assign")
async def addcolorreactionroleCommand(
    interaction: discord.Interaction, emoji: str, role: discord.Role
):
    await addReactionRole.addcolorreactionrole(
        interaction=interaction, emoji=emoji, role=role
    )


# ───── Run the Bot ─────
bot.run(token)
