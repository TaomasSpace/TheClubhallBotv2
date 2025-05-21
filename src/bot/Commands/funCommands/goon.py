import discord
from random import random

# Sends a "goon" interaction between two users with a 95% success rate
async def goon(interaction: discord.Interaction, user: discord.Member):
    sender_id = interaction.user.id

    try:
        # Prevent users from targeting themselves
        if user.id == sender_id:
            await interaction.response.send_message(
                "You can't goon to yourself", ephemeral=True
            )
            return

        chance = 0.95  # 95% success chance
        if random() < chance:
            # Successful goon
            embed = discord.Embed(
                title=f"{interaction.user.display_name} goons to {user.display_name}!",
                color=discord.Color.red(),
            )
        else:
            # Failure case: gooner dies
            embed = discord.Embed(
                title=f"{interaction.user.display_name} dies because of gooning!",
                color=discord.Color.red(),
            )

        await interaction.response.send_message(embed=embed)

    except:
        # Generic failure response (ideally log exception in production)
        await interaction.response.send_message(
            "Command didn't work, sorry :(", ephemeral=True
        )
