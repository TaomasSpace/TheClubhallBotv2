import discord
from helper.helper import has_role
from Database.databaseHelper import set_boost_level
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")
ADMIN_ROLE_NAME = os.getenv("ADMIN_ROLE_NAME")

async def setboostlevel(
    interaction: discord.Interaction, user: discord.Member, level: int
):
    if not has_role(interaction.user, ADMIN_ROLE_NAME):
        await interaction.response.send_message("No permission.", ephemeral=True)
        return

    if level not in (1, 2, 3):
        await interaction.response.send_message(
            "Only levels 1, 2, or 3 are allowed.", ephemeral=True
        )
        return

    set_boost_level(str(user.id), level)
    await interaction.response.send_message(
        f"✅ Boost level for {user.display_name} set to {level}.", ephemeral=True
    )