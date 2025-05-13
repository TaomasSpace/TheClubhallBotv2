import discord
import helper.gifs
from random import random, choice, randint

async def punch(interaction: discord.Interaction, user: discord.Member):

    if user.id == interaction.user.id:
        await interaction.response.send_message(
            "You can't punch yourself ... or maybe you can?", ephemeral=True
        )
        return

    selected_gif = choice(helper.gifs.punch_gifs)
    embed = discord.Embed(
        title=f"{interaction.user.display_name} punches {user.display_name}!",
        color=discord.Colour.red(),
    )
    embed.set_image(url=selected_gif)

    await interaction.response.send_message(embed=embed)