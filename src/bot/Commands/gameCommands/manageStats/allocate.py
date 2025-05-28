import discord
from Database.databaseHelper import register_user, increase_stat, get_stats
from helper.helper import sync_stat_roles
import configparser
from pathlib import Path

CONFIG_PATH = Path(__file__).parents[3] / "config.ini"
config = configparser.ConfigParser()
config.optionxform = str
if CONFIG_PATH.is_file():
    config.read(CONFIG_PATH)

STAT_NAMES = [
    stat.strip().lower() for stat in config["Gameconfigs"]["STAT_NAMES"].split(",")
]


async def allocate(interaction: discord.Interaction, stat: str, points: int):
    stat = stat.lower()
    if stat not in STAT_NAMES:
        await interaction.response.send_message("Invalid stat name.", ephemeral=True)
        return
    if points < 1:
        await interaction.response.send_message("Points must be > 0.", ephemeral=True)
        return

    await interaction.response.defer(thinking=True, ephemeral=True)

    uid = str(interaction.user.id)
    register_user(uid, interaction.user.display_name)
    user_stats = get_stats(uid)

    if user_stats["stat_points"] < points:
        await interaction.followup.send("Not enough unspent points.")
        return

    increase_stat(uid, stat, points)
    await sync_stat_roles(interaction.user)

    await interaction.followup.send(f"🔧 {stat.title()} increased by {points}.")
