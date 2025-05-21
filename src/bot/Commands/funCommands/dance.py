import discord
from random import choice
import helper.gifs

# Sends a random dance GIF in an embedded message
async def dance(interaction: discord.Interaction):
    try:
        gif_url = choice(helper.gifs.dance_gifs)

        if gif_url:
            embed = discord.Embed(
                title=f"{interaction.user.display_name} Dances",
                color=discord.Color.red(),
            )
            embed.set_image(url=gif_url)
            print(gif_url)  # Optional: remove or replace with logging in production
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(
                "No Dance GIFs found in the database.", ephemeral=False
            )
    except:
        # Catch-all error handling (consider logging the exception in real use)
        await interaction.response.send_message(
            "Command didn't work, sorry :(", ephemeral=True
        )
