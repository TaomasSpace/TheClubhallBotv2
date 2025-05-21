import discord
import helper.gifs
from random import random, choice, randint

# Sends a "punch" interaction with a random punch GIF between two users
async def punch(interaction: discord.Interaction, user: discord.Member):
    # Prevent self-targeting (for fun, message hints ambiguity)
    if user.id == interaction.user.id:
        await interaction.response.send_message(
            "You can't punch yourself ... or maybe you can?", ephemeral=True
        )
        return

    # Select a random punch GIF
    selected_gif = choice(helper.gifs.punch_gifs)

    # Build and send the embed
    embed = discord.Embed(
        title=f"{interaction.user.display_name} punches {user.display_name}!",
        color=discord.Colour.red(),
    )
    embed.set_image(url=selected_gif)

    await interaction.response.send_message(embed=embed)
