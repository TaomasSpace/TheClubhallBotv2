import discord
import os
from helper.helper import get_channel_webhook, has_role
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


async def imitate(interaction: discord.Interaction, user: discord.Member, msg: str):
    ADMIN_ROLE_NAME = os.getenv("ADMIN_ROLE_NAME")
    if not has_role(interaction.user, ADMIN_ROLE_NAME):
        await interaction.response.send_message(
            "You don't have permission to use this command.", ephemeral=True
        )
        return

    channel = interaction.channel
    webhook = await get_channel_webhook(channel)

    try:
        await webhook.send(
            content=msg,
            username=user.display_name,
            avatar_url=user.display_avatar.url,
            allowed_mentions=discord.AllowedMentions.none(),
        )
        await interaction.response.send_message("✅ Message sent.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Failed to imitate: {e}", ephemeral=True
        )
