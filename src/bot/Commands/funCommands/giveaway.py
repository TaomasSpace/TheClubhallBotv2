import discord
from helper.helper import has_role
import os
from random import choice
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=".env")

# Admin-only command to start a timed giveaway with emoji-based participation
async def giveaway(interaction: discord.Interaction, duration: int, prize: str):
    ADMIN_ROLE_NAME = os.getenv("ADMIN_ROLE_NAME")

    # Check if the user has the required admin role
    if not has_role(interaction.user, ADMIN_ROLE_NAME):
        await interaction.response.send_message(
            "Only admins and owners can use this command", ephemeral=True
        )
        return

    # Build the giveaway embed
    embed = discord.Embed(
        title="🎉 GIVEAWAY 🎉",
        description=(
            f"React with 🎉 to win **{prize}**!\n"
            f"🔔 Duration: **{duration} min**."
        ),
        color=discord.Color.gold(),
    )
    embed.set_footer(
        text=f"Created by: {interaction.user.display_name}",
        icon_url=interaction.user.display_avatar.url,
    )

    # Send the giveaway message and add the reaction
    await interaction.response.send_message(embed=embed)
    giveaway_msg = await interaction.original_response()
    await giveaway_msg.add_reaction("🎉")

    # Wait for the giveaway duration
    await asyncio.sleep(duration * 60)

    # Fetch the message again to get updated reactions
    refreshed = await giveaway_msg.channel.fetch_message(giveaway_msg.id)
    reaction = discord.utils.get(refreshed.reactions, emoji="🎉")

    # Check if anyone participated
    if reaction is None:
        await refreshed.reply("No one has participated.")
        return

    users = [u async for u in reaction.users() if not u.bot]
    if not users:
        await refreshed.reply("No one has participated.")
        return

    # Select a random non-bot winner
    winner = choice(users)
    await refreshed.reply(
        f"🎊 Congratulations {winner.mention}! "
        f"You have won **{prize}** 🎉"
    )
