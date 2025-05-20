from dotenv import load_dotenv
import os
import discord
from helper.helper import has_role
from Database.databaseHelper import get_money, set_money

# Load environment variables
load_dotenv(dotenv_path=".env")

ADMIN_ROLE_NAME = os.getenv("ADMIN_ROLE_NAME")
BOT_USERID = os.getenv("BOT_USERID")

# Removes coins from a user and transfers them to the server's bank (admin-only)
async def remove(interaction: discord.Interaction, user: discord.Member, amount: int):
    # Permission check for admin role
    if not has_role(interaction.user, ADMIN_ROLE_NAME):
        await interaction.response.send_message(
            "You don't have permission to remove clubhall coins.", ephemeral=True
        )
        return

    uid = str(user.id)

    # Get current balances
    current = get_money(uid)
    current_bank = get_money(BOT_USERID)

    # Calculate how much can actually be removed (avoid negative balance)
    to_remove = min(amount, current)

    # Apply balance changes
    set_money(uid, current - to_remove)
    set_money(BOT_USERID, current_bank + to_remove)

    # Notify success
    await interaction.response.send_message(
        f"💸 {to_remove} clubhall coins removed from {user.display_name} and added to the bank."
    )
