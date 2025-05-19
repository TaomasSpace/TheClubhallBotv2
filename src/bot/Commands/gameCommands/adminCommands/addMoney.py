from dotenv import load_dotenv
import os
import discord
from helper.helper import has_role, safe_add_coins
from Database.databaseHelper import register_user

load_dotenv(dotenv_path=".env")

ADMIN_ROLE_NAME = os.getenv("ADMIN_ROLE_NAME")


async def addMoney(interaction: discord.Interaction, user: discord.Member, amount: int):
    if not has_role(interaction.user, ADMIN_ROLE_NAME):
        await interaction.response.send_message(
            "You don't have permission to give clubhall coins.", ephemeral=True
        )
        return

    register_user(str(user.id), user.display_name)
    added = safe_add_coins(str(user.id), amount)
    if added == 0:
        await interaction.response.send_message(
            f"Clubhall coin limit reached. No coins added.", ephemeral=True
        )
    elif added < amount:
        await interaction.response.send_message(
            f"Partial success: Only {added} coins added due to server limit.",
            ephemeral=True,
        )
    else:
        await interaction.response.send_message(
            f"{added} clubhall coins added to {user.display_name}."
        )
