import discord
from Database.databaseHelper import get_custom_role


# Allows a booster to share their custom role with another member, based on boost level
async def grantrole(interaction: discord.Interaction, target: discord.Member):
    booster_id = str(interaction.user.id)
    target_id = str(target.id)

    # Prevent user from assigning the role to themselves
    if booster_id == target_id:
        await interaction.response.send_message(
            "You can't give your role to yourself.", ephemeral=True
        )
        return

    # Fetch the booster’s custom role
    role_id = get_custom_role(booster_id)
    if not role_id:
        await interaction.response.send_message(
            "You don't have a custom role.", ephemeral=True
        )
        return

    role = interaction.guild.get_role(role_id)
    if not role:
        await interaction.response.send_message(
            "Your custom role was not found.", ephemeral=True
        )
        return

    # Grant the role to the target member
    await target.add_roles(role, reason="Booster shared custom role")
    await interaction.response.send_message(
        f"✅ {target.display_name} got your role **{role.name}**.", ephemeral=False
    )
