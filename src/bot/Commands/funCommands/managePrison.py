import discord
from helper.helper import has_role
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv(dotenv_path=".env")
ADMIN_ROLE_NAME = os.getenv("ADMIN_ROLE_NAME")


async def managePrisonMember(interaction: discord.Interaction, user: discord.Member):
    if not has_role(interaction.user, ADMIN_ROLE_NAME):
        await interaction.response.send_message("No permission.", ephemeral=True)
        return

    role_name = "Guest of the Clubhall"
    role = discord.utils.get(interaction.guild.roles, name=role_name)

    if not role:
        await interaction.response.send_message(
            f"❌ Role '{role_name}' not found.", ephemeral=True
        )
        return

    if role in user.roles:
        await user.remove_roles(role)
        await interaction.response.send_message(
            f"🔒 {user.mention} has been sent to prison.", ephemeral=False
        )
    else:
        await user.add_roles(role)
        await interaction.response.send_message(
            f"🔓 {user.mention} has been freed from prison.", ephemeral=False
        )
