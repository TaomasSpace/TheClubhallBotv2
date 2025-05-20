import discord
from Database.databaseHelper import get_custom_role, get_boost_level, _fetchone

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

    # Enforce minimum boost level requirement
    if get_boost_level(booster_id) < 2:
        await interaction.response.send_message(
            "You need boost level 2 to give your role to others.", ephemeral=True
        )
        return

    role = interaction.guild.get_role(role_id)
    if not role:
        await interaction.response.send_message(
            "Your custom role was not found.", ephemeral=True
        )
        return

    # Count how many users currently have this role (excluding the booster themself)
    assigned_users = _fetchone(
        "SELECT COUNT(*) FROM custom_roles WHERE role_id = ? AND user_id != ?",
        (role_id, booster_id),
    )[0]

    # Limit role sharing based on boost level
    if get_boost_level(booster_id) == 2:
        if assigned_users >= 2:
            await interaction.response.send_message(
                "You can only give your role to 2 other people. (Get booster level 3 to share it with up to 5 people)",
                ephemeral=True,
            )
            return
    elif get_boost_level(booster_id) == 3:
        if assigned_users >= 5:
            await interaction.response.send_message(
                "You can only give your role to 5 other people.", ephemeral=True
            )
            return

    # Grant the role to the target member
    await target.add_roles(role, reason="Booster shared custom role")
    await interaction.response.send_message(
        f"✅ {target.display_name} got your role **{role.name}**.", ephemeral=False
    )
