from dotenv import load_dotenv
import os
import discord
<<<<<<< Updated upstream
<<<<<<< Updated upstream
from discord.ext import commands
<<<<<<< Updated upstream
import helper.events
from bot_instance import bot
=======

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
=======
=======
>>>>>>> Stashed changes
from discord import app_commands
from bot_instance import bot
import helper.events
from Commands.boosterPearks.setBoostLevel import setboostlevel
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes

load_dotenv(dotenv_path=".env")
token = os.getenv("bot_token")

<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot is online as {bot.user}")

=======
=======
>>>>>>> Stashed changes
@bot.tree.command(
    name="setboostlevel", description="Set custom boost level manually (Admin only)"
)
@app_commands.describe(user="User", level="Boost level (1, 2, or 3)")
async def setboostlevelCommand(
    interaction: discord.Interaction, user: discord.Member, level: int
):
    await setboostlevel(interaction=interaction, user=user, level=level)
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

>>>>>>> Stashed changes
bot.run(token)