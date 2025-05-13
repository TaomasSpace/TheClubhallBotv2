import discord
from helper.helper import has_role
from dotenv import load_dotenv
import os
from random import choice
import asyncio

async def giveaway(interaction: discord.Interaction, duration: int, prize: str):
    load_dotenv(dotenv_path=".env")
    ADMIN_ROLE_NAME = os.getenv("ADMIN_ROLE_NAME")

    if not has_role(interaction.user, ADMIN_ROLE_NAME):
        await interaction.response.send_message(
            "Only admins and owners can use this command", ephemeral=True
        )
        return

    embed = discord.Embed(
        title="🎉 GIVEAWAY 🎉",
        description=(
            f"React with 🎉 to win **{prize}**!\n" f"🔔 Duration: **{duration} min**."
        ),
        color=discord.Color.gold(),
    )
    embed.set_footer(
        text=f"Created by: {interaction.user.display_name}",
        icon_url=interaction.user.display_avatar.url,
    )

    await interaction.response.send_message(embed=embed)
    giveaway_msg = await interaction.original_response()
    await giveaway_msg.add_reaction("🎉")

    await asyncio.sleep(duration * 60)

    refreshed = await giveaway_msg.channel.fetch_message(giveaway_msg.id)

    reaction = discord.utils.get(refreshed.reactions, emoji="🎉")
    if reaction is None:
        await refreshed.reply("No one has participated.")
        return

    users = [u async for u in reaction.users() if not u.bot]
    if not users:
        await refreshed.reply("No one has participated.")
        return

    winner = choice(users)
    await refreshed.reply(
        f"🎊 Congratulation! {winner.mention}! " f"You have won **{prize}** 🎉"
    )
