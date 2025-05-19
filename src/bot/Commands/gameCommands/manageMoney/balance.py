import discord
from Database.databaseHelper import register_user, get_money


async def balance(interaction: discord.Interaction, user: discord.Member):
    register_user(str(user.id), user.display_name)
    money = get_money(str(user.id))
    print(user.id)
    await interaction.response.send_message(
        f"{user.display_name} has {money} clubhall coins."
    )
