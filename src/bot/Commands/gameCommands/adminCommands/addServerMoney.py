from dotenv import load_dotenv
import os
import discord
from helper.helper import has_role, safe_add_coins
from Database.databaseHelper import register_user

load_dotenv(dotenv_path=".env")

ADMIN_ROLE_NAME = os.getenv("ADMIN_ROLE_NAME")
BOT_USERID = os.getenv("BOT_USERID")


async def addServerMoney(interaction: discord.Interaction, amount: int):
    if not has_role(interaction.user, ADMIN_ROLE_NAME):
        await interaction.response.send_message(
            "You don't have permission to add clubhall coins.", ephemeral=True
        )
        return

    added = safe_add_coins(BOT_USERID, amount)
    await interaction.response.send_message(
        f"{added} coins added to the bank", ephemeral=True
    )
