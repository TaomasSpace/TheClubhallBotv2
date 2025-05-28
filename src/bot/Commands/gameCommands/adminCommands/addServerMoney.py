from dotenv import load_dotenv
import os
import discord
from helper.helper import has_role, safe_add_coins

# Load environment variables
load_dotenv(dotenv_path=".env")

ADMIN_ROLE_NAME = os.getenv("ADMIN_ROLE_NAME")
BOT_USERID = os.getenv("BOT_USERID")  # Used as the server/bank account ID


# Adds coins to the server’s central bank account (admin-only)
async def addServerMoney(interaction: discord.Interaction, amount: int):
    # Verify that the user has admin privileges
    if not has_role(interaction.user, ADMIN_ROLE_NAME):
        await interaction.response.send_message(
            "You don't have permission to add clubhall coins.", ephemeral=True
        )
        return

    # Add coins to the server/bank account (tracked using the bot’s user ID)
    added = safe_add_coins(BOT_USERID, amount)

    await interaction.response.send_message(
        f"{added} coins added to the bank", ephemeral=True
    )
