import discord
from random import random


async def goon(interaction: discord.Interaction, user: discord.Member):

    sender_id = interaction.user.id
    try:
        if user.id == sender_id:
            await interaction.response.send_message(
                "You cant goon to yourself", ephemeral=True
            )

        chance = 0.95
        if random() < chance:
            embed = discord.Embed(
                title=f"{interaction.user.display_name} goons to {user.display_name}!",
                color=discord.Color.red(),
            )
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title=f"{interaction.user.display_name} dies because of gooning!",
                color=discord.Color.red(),
            )
            await interaction.response.send_message(embed=embed)
    except:
        await interaction.response.send_message(
            "Command didnt work, sry :(", ephemeral=True
        )
