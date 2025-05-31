import discord
import os
from helper.helper import get_channel_webhook, has_role
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=".env")

# Sends a message via webhook that mimics another user (admin-only)
async def imitate(interaction: discord.Interaction, user: discord.Member, msg: str):
    ADMIN_ROLE_NAME = os.getenv("ADMIN_ROLE_NAME")

    # Permission check: only users with the admin role may execute this command
    if not has_role(interaction.user, ADMIN_ROLE_NAME) and not interaction.user.premium_since:
        await interaction.response.send_message(
            "You don't have permission to use this command.", ephemeral=True
        )
        return

    channel = interaction.channel
    webhook = await get_channel_webhook(channel)

    try:
        # Send message using the webhook, imitating the target user
        await webhook.send(
            content=msg,
            username=user.display_name,
            avatar_url=user.display_avatar.url,
            allowed_mentions=discord.AllowedMentions.none(),  # Prevent ping abuse
        )
        await interaction.response.send_message("✅ Message sent.", ephemeral=True)

    except Exception as e:
        # Gracefully handle errors and inform the command issuer
        await interaction.response.send_message(
            f"❌ Failed to imitate: {e}", ephemeral=True
        )
