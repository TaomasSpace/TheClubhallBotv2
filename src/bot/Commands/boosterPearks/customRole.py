import discord
from Database.databaseHelper import get_custom_role, set_custom_role

# Handles the creation or update of a custom role for server boosters
async def customrole(interaction: discord.Interaction, name: str, color: str):
    member = interaction.user
    guild = interaction.guild

    # Restrict command usage to server boosters
    if not member.premium_since:
        await interaction.response.send_message(
            "❌ This command is only for server boosters!", ephemeral=True
        )
        return

    # Attempt to parse the hex color string to a Discord Colour object
    try:
        colour_obj = discord.Colour(int(color.lstrip("#"), 16))
    except ValueError:
        await interaction.response.send_message(
            "⚠️ Invalid color. Use hex like #FFAA00", ephemeral=True
        )
        return

    # Check if the user already has a custom role saved in the database
    role_id = get_custom_role(str(member.id))

    if role_id:
        role = guild.get_role(role_id)
        if role:
            # If role exists, update its name and color
            await role.edit(name=name, colour=colour_obj)
            await interaction.response.send_message(
                f"🔄 Your role has been updated to **{name}**.", ephemeral=True
            )
            return

    # If no existing role, create a new one and assign it to the member
    try:
        role = await guild.create_role(
            name=name, colour=colour_obj, reason="Custom booster role"
        )
        await member.add_roles(role, reason="Assigned custom booster role")
        set_custom_role(str(member.id), role.id)
        await interaction.response.send_message(
            f"✅ Custom role **{name}** created and assigned!", ephemeral=True
        )
    except discord.Forbidden:
        # Handle insufficient permission to manage roles
        await interaction.response.send_message(
            "❌ I need permission to manage roles.", ephemeral=True
        )
