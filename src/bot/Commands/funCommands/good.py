import discord
from random import choice
from helper.helper import has_role
from helper.gifs import sheher_gifs, hehim_gifs
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=".env")

# Sends a gender-personalized "good [X]" message with a matching GIF
async def good(interaction: discord.Interaction, user: discord.Member):
    SHEHER_ROLE_NAME = os.getenv("SHEHER_ROLE_NAME")
    HEHIM_ROLE_NAME = os.getenv("HEHIM_ROLE_NAME")
    undefined_gifs = sheher_gifs + hehim_gifs

    try:
        # If user has she/her role → send "good girl" message
        if has_role(user, SHEHER_ROLE_NAME):
            gif_url = choice(sheher_gifs)
            if gif_url:
                embed = discord.Embed(
                    title=f"{interaction.user.display_name} calls {user.display_name} a good girl",
                    color=discord.Color.red(),
                )
                embed.set_image(url=gif_url)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(
                    "No good girl GIFs found in the database.", ephemeral=False
                )

        # If user has he/him role → send "good boy" message
        elif has_role(user, HEHIM_ROLE_NAME):
            gif_url = choice(hehim_gifs)
            if gif_url:
                embed = discord.Embed(
                    title=f"{interaction.user.display_name} calls {user.display_name} a good boy",
                    color=discord.Color.red(),
                )
                embed.set_image(url=gif_url)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(
                    "No good boy GIFs found in the database.", ephemeral=False
                )

        # If user has neither role → send neutral "good child" message
        else:
            gif_url = choice(undefined_gifs)
            if gif_url:
                embed = discord.Embed(
                    title=f"{interaction.user.display_name} calls {user.display_name} a good child",
                    color=discord.Color.red(),
                )
                embed.set_image(url=gif_url)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(
                    "No good person GIFs found in the database.", ephemeral=False
                )

    except:
        # Generic error handler (ideally should catch specific exceptions and log)
        await interaction.response.send_message(
            "Command didn't work, sorry :(", ephemeral=True
        )
