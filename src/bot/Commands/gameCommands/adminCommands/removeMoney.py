from dotenv import load_dotenv
import os
import discord
from helper.helper import has_role
from Database.databaseHelper import get_money, set_money

load_dotenv(dotenv_path=".env")

ADMIN_ROLE_NAME = os.getenv("ADMIN_ROLE_NAME")
BOT_USERID = os.getenv("BOT_USERID")

async def remove(interaction: discord.Interaction, user: discord.Member, amount: int):
    if not has_role(interaction.user, ADMIN_ROLE_NAME):
        await interaction.response.send_message(
            "You don't have permission to remove clubhall coins.", ephemeral=True
        )
        return

    uid = str(user.id)
    current = get_money(uid)
    current_bank = get_money(BOT_USERID)

    to_remove = min(amount, current)

    set_money(uid, current - to_remove)
    set_money(BOT_USERID, current_bank + to_remove)

    await interaction.response.send_message(
        f"💸 {to_remove} clubhall coins removed from {user.display_name} and added to the bank."
    )
