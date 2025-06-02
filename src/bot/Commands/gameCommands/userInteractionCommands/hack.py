import discord
from Database.databaseHelper import register_user, get_stats, set_money, get_money
from helper.helper import safe_add_coins
from random import randint


async def hack(interaction: discord.Interaction):
    uid = str(interaction.user.id)
    register_user(uid, interaction.user.display_name)

    stats = get_stats(uid)
    if stats["intelligence"] < 5:
        await interaction.response.send_message(
            "❌ You need at least **5** Intelligence to attempt a hack.", ephemeral=True
        )
        return

    int_level = stats["intelligence"]
    success = 10  # TODO: here algorith for the amount!!

    if not success:
        loss = randint(1, 5) * int_level
        new_bal = max(0, get_money(uid) - loss)
        set_money(uid, new_bal)
        await interaction.response.send_message(
            f"💻 Hack failed! Security traced you and you lost **{loss}** coins.",
            ephemeral=True,
        )
        return

    reward = randint(5, 12) * int_level
    added = safe_add_coins(uid, reward)

    if added > 0:
        await interaction.response.send_message(
            f"🔋 Hack successful! You siphoned **{added}** coins from the bank.",
            ephemeral=True,
        )
    else:
        await interaction.response.send_message(
            "⚠️ Hack succeeded but server coin limit reached. No coins added.",
            ephemeral=True,
        )
