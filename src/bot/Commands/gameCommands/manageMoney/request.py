import discord
from Database.databaseHelper import register_user
from helper.helper import RequestView

# Sends a coin request from one user to another with an interactive approval view
async def request(
    interaction: discord.Interaction, user: discord.Member, amount: int, reason: str
):
    sender_id = interaction.user.id
    receiver_id = user.id

    # Prevent users from requesting coins from themselves
    if sender_id == receiver_id:
        await interaction.response.send_message(
            "You can't request clubhall coins from yourself.", ephemeral=True
        )
        return

    # Ensure both users are registered
    register_user(str(sender_id), interaction.user.display_name)
    register_user(str(receiver_id), user.display_name)

    # Send interactive request message with custom view for approval/denial
    view = RequestView(sender_id, receiver_id, amount)
    await interaction.response.send_message(
        f"{user.mention}, {interaction.user.display_name} requests **{amount}** clubhall coins for: _{reason}_",
        view=view,
    )
