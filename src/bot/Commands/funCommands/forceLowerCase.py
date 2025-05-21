import discord
from helper.helper import lowercase_locked

# Toggles forced lowercase message formatting for a specified member
async def forcelowercase(interaction: discord.Interaction, member: discord.Member):
    if member.id in lowercase_locked:
        # Remove from lock set – messages will no longer be forced to lowercase
        lowercase_locked.remove(member.id)
        await interaction.response.send_message(
            f"🔓 {member.display_name} unlocked – messages stay unchanged.",
            ephemeral=True,
        )
    else:
        # Add to lock set – messages will be forced to lowercase
        lowercase_locked.add(member.id)
        await interaction.response.send_message(
            f"🔒 {member.display_name} locked – messages will be lower‑cased.",
            ephemeral=True,
        )
