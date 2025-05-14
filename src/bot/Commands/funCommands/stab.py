import discord
from random import random, choice, randint
import helper.helper
import os
from helper.gifs import special_gifs, stab_gifs

OWNER_ROLE_NAME = os.getenv("OWNER_ROLE_NAME")


async def stab(interaction: discord.Interaction, user: discord.Member):

    sender_id = interaction.user.id
    try:
        if user.id == sender_id:
            chance = 0.20
            if helper.helper.has_role(interaction.user, OWNER_ROLE_NAME):
                chance = 0.75

            if random() < chance:
                selected_gif = choice(special_gifs)
                embed = discord.Embed(
                    title=f"{interaction.user.display_name} tried to stab themselves... and succeeded?!",
                    color=discord.Color.red(),
                )
                embed.set_image(url=selected_gif)
                await interaction.response.send_message(embed=embed)
                return
            else:
                await interaction.response.send_message(
                    "You can't stab yourself... or can you?", ephemeral=True
                )
                return

        chance = 0.50
        if helper.helper.has_role(interaction.user, OWNER_ROLE_NAME):
            chance = 0.90
        if random() < chance:
            gif_url = choice(stab_gifs)
            if gif_url:
                embed = discord.Embed(
                    title=f"{interaction.user.display_name} stabs {user.display_name}!",
                    color=discord.Color.red(),
                )
                embed.set_image(url=gif_url)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(
                    "No stab GIFs found in the database.", ephemeral=True
                )
        else:
            fail_messages = [
                "Isn't that illegal?",
                "You don't have a knife.",
                "You missed completely!",
                "They dodged like a ninja!",
                "You changed your mind last second.",
                "Your knife broke!",
            ]
            await interaction.response.send_message(choice(fail_messages))
    except Exception as e:
        print("Fehler im stab-Command:", e)
        await interaction.response.send_message(
            "Something went wrong during the stabbing attempt. Contact an admin.",
            ephemeral=True,
        )
