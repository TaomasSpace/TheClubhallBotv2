import discord
from Database.databaseHelper import register_user, get_money, set_money
from helper.helper import safe_add_coins

# Allows a user to donate clubhall coins to another member
async def donate(interaction: discord.Interaction, user: discord.Member, amount: int):
    sender_id = str(interaction.user.id)
    receiver_id = str(user.id)

    # Prevent self-donation
    if sender_id == receiver_id:
        await interaction.response.send_message(
            "You can't donate coins to yourself.", ephemeral=True
        )
        return

    # Ensure both users are registered in the database
    register_user(sender_id, interaction.user.display_name)
    register_user(receiver_id, user.display_name)

    sender_balance = get_money(sender_id)

    # Validate donation amount
    if amount <= 0:
        await interaction.response.send_message(
            "Amount must be greater than 0.", ephemeral=True
        )
        return

    if amount > sender_balance:
        await interaction.response.send_message(
            "You don't have enough clubhall coins.", ephemeral=True
        )
        return

    # Perform transaction
    set_money(sender_id, sender_balance - amount)
    safe_add_coins(receiver_id, amount)

    # Confirm transaction
    await interaction.response.send_message(
        f"💸 You donated **{amount}** clubhall coins to {user.display_name}!",
        ephemeral=False,
    )
