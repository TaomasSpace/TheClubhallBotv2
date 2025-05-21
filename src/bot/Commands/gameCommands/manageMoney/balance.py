import discord
from Database.databaseHelper import register_user, get_money

# Displays the clubhall coin balance of a user
async def balance(interaction: discord.Interaction, user: discord.Member):
    # Ensure user is registered in the database
    register_user(str(user.id), user.display_name)

    # Retrieve current balance
    money = get_money(str(user.id))

    print(user.id)  # Consider removing or replacing with proper logging in production

    # Send the balance information
    await interaction.response.send_message(
        f"{user.display_name} has {money} clubhall coins."
    )
