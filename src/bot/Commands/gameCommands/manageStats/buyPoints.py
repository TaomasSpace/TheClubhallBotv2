import discord
import math
from Database.databaseHelper import register_user, set_money, get_money, add_stat_points


async def buypoints(interaction: discord.Interaction, amount: int = 1):
    if amount < 1:
        await interaction.response.send_message(
            "Specify a positive amount.", ephemeral=True
        )
        return
    uid = str(interaction.user.id)
    register_user(uid, interaction.user.display_name)

    price_per_point = kosten(amount)
    cost = price_per_point * amount
    balance = get_money(uid)
    if balance < cost:
        await interaction.response.send_message(
            f"❌ You need {cost} coins but only have {balance}.", ephemeral=True
        )
        return
    set_money(uid, balance - cost)
    add_stat_points(uid, amount)
    await interaction.response.send_message(
        f"✅ Purchased {amount} point(s) for {cost} coins."
    )


def kosten(x):
    return int(15 * math.exp(0.01113 * (x - 1)))
