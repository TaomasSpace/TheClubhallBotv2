import discord

def has_role(member: discord.Member, role_name: str):
    return any(role.name == role_name for role in member.roles)