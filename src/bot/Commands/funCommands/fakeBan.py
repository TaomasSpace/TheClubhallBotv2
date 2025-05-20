import discord
from helper.helper import get_channel_webhook, has_role
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=".env")
ADMIN_ROLE_NAME = os.getenv("ADMIN_ROLE_NAME")

# Simulates a ban message via webhook (no actual ban occurs)
async def fakeBan(interaction: discord.Interaction, user: discord.Member, reason: str):
    # Permission check: only users with the admin role can use this command
    if not has_role(interaction.user, ADMIN_ROLE_NAME):
        await interaction.response.send_message(
            "You don't have permission to use this command.", ephemeral=True
        )
        return

    try:
        # Defer the response to allow for async processing
        await interaction.response.defer(ephemeral=True)

        # Retrieve or create a webhook for the current channel
        webhook = await get_channel_webhook(interaction.channel)
        if webhook is None:
            await interaction.followup.send(
                "❌ Webhook not found or could not be created.", ephemeral=True
            )
            return

        # Send the fake ban message via the webhook
        await webhook.send(
            f"🚫 {user.mention} has been permanently banned by {interaction.user.mention} for '{reason}'.",
            username="MEMBER MODERATION",
            avatar_url="https://i.imgur.com/AfFp7pu.png",
        )

        await interaction.followup.send("✅ Fake ban sent.", ephemeral=True)

    except Exception as e:
        # Log the error and notify the user
        print("Fakeban error:", e)
        try:
            await interaction.followup.send(
                f"❌ Failed to fake ban: {e}", ephemeral=True
            )
        except:
            pass  # Suppress any further errors silently
