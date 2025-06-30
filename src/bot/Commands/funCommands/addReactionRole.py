import discord
from helper.helper import has_role
from Database.databaseHelper import _execute
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=".env")
ADMIN_ROLE_NAME = os.getenv("ADMIN_ROLE_NAME")


async def addcolorreactionrole(
    interaction: discord.Interaction,
    target_message_id: int,
    emoji: str,
    role: discord.Role,
):
    if not has_role(interaction.user, ADMIN_ROLE_NAME):
        await interaction.response.send_message("No permission.", ephemeral=True)
        return

    channel = interaction.channel
    try:
        message = await channel.fetch_message(target_message_id)
        await message.add_reaction(emoji)

        _execute(
            "INSERT OR REPLACE INTO reaction_roles (message_id, emoji, role_id) VALUES (?, ?, ?)",
            (str(target_message_id), emoji, str(role.id)),
        )

        await interaction.response.send_message(
            f"✅ Added emoji {emoji} for role {role.name}.", ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)
