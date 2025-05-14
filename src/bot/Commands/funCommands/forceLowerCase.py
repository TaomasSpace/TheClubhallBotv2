import discord
from helper.helper import lowercase_locked


async def forcelowercase(interaction: discord.Interaction, member: discord.Member):

    if member.id in lowercase_locked:
        lowercase_locked.remove(member.id)
        await interaction.response.send_message(
            f"🔓 {member.display_name} unlocked – messages stay unchanged.",
            ephemeral=True,
        )
    else:
        lowercase_locked.add(member.id)
        await interaction.response.send_message(
            f"🔒 {member.display_name} locked – messages will be lower‑cased.",
            ephemeral=True,
        )
