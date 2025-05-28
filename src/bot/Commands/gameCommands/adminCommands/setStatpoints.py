import discord
from helper.helper import has_role
from Database.databaseHelper import register_user, _execute
from dotenv import load_dotenv
import os
import configparser
from pathlib import Path

CONFIG_PATH = Path(__file__).parents[3] / "config.ini"
config = configparser.ConfigParser()
config.optionxform = str
if CONFIG_PATH.is_file():
    config.read(CONFIG_PATH)

load_dotenv(dotenv_path=".env")

ADMIN_ROLE_NAME = os.getenv("ADMIN_ROLE_NAME")
STAT_NAMES = [
    stat.strip().lower() for stat in config["Gameconfigs"]["STAT_NAMES"].split(",")
]


async def setstat(
    interaction: discord.Interaction,
    user: discord.Member,
    stat: str | None,
    amount: int,
):
    if not has_role(interaction.user, ADMIN_ROLE_NAME):
        await interaction.response.send_message(
            "Only the Admins can use this command.", ephemeral=True
        )
        return

    if amount < 0:
        await interaction.response.send_message("Amount must be ≥ 0.", ephemeral=True)
        return

    uid = str(user.id)
    register_user(uid, user.display_name)

    if stat:
        stat = stat.lower()
        if stat not in STAT_NAMES:
            await interaction.response.send_message(
                "Invalid stat name.", ephemeral=True
            )
            return

        _execute(f"UPDATE users SET {stat} = ? WHERE user_id = ?", (amount, uid))
        await interaction.response.send_message(
            f"✅ Set {user.display_name}'s **{stat}** to **{amount}**.", ephemeral=True
        )
    else:
        _execute("UPDATE users SET stat_points = ? WHERE user_id = ?", (amount, uid))
        await interaction.response.send_message(
            f"✅ Set {user.display_name}'s **stat points** to **{amount}**.",
            ephemeral=True,
        )
