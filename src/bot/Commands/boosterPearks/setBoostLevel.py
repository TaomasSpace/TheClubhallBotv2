import discord
from helper.helper import has_role
from Database.databaseHelper import set_boost_level
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(dotenv_path=".env")
ADMIN_ROLE_NAME = os.getenv("ADMIN_ROLE_NAME")

# Admin-only command to manually assign a boost level to a user
async def setboostlevel(
    interaction: discord.Interaction, user: discord.Member, level: int
):
    # Check if the invoking user has the required admin role
    if not has_role(interaction.user, ADMIN_ROLE_NAME):
        await interaction.response.send_message("No permission.", ephemeral=True)
        return

    # Only allow valid boost levels
    if level not in (1, 2, 3):
        await interaction.response.send_message(
            "Only levels 1, 2, or 3 are allowed.", ephemeral=True
        )
        return

    # Update the user's boost level in the database
    set_boost_level(str(user.id), level)
    await interaction.response.send_message(
        f"✅ Boost level for {user.display_name} set to {level}.", ephemeral=True
    )
