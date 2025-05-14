import discord
from helper.helper import get_channel_webhook, has_role
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
ADMIN_ROLE_NAME = os.getenv("ADMIN_ROLE_NAME")


async def fakeBan(interaction: discord.Interaction, user: discord.Member, reason: str):
    if not has_role(interaction.user, ADMIN_ROLE_NAME):
        await interaction.response.send_message(
            "You don't have permission to use this command.", ephemeral=True
        )
        return

    try:
        await interaction.response.send_message(
            f"🚫 {user.mention} has been permanently banned by {interaction.user.mention} for '{reason}'.",
            ephemeral=False,
        )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Failed to fake ban: {e}", ephemeral=True
        )
