import discord

def has_role(member: discord.Member, role_name: str):
    return any(role.name == role_name for role in member.roles)

TRIGGER_RESPONSES = {
    "シャドウストーム": "Our beautiful majestic Emperor シャドウストーム! Long live our beloved King 👑",
    "goodyb": "Our beautiful majestic Emperor goodyb! Long live our beloved King 👑",
    "shadow": "Our beautiful majestic Emperor TAOMA™! Long live our beloved King 👑",
    "taoma": "Our beautiful majestic Emperor TAOMA™! Long live our beloved King 👑",
    "Taoma": "Our beautiful majestic Emperor TAOMA™! Long live our beloved King 👑",
    " King": "Our beautiful majestic Emperor TAOMA™! Long live our beloved King 👑",
}

lowercase_locked: set[int] = set()
webhook_cache: dict[int, discord.Webhook] = {}

async def get_channel_webhook(channel: discord.TextChannel) -> discord.Webhook:
    wh = webhook_cache.get(channel.id)
    if wh:
        return wh
    webhooks = await channel.webhooks()
    wh = discord.utils.get(
        webhooks, name="LowercaseRelay"
    ) or await channel.create_webhook(name="LowercaseRelay")
    webhook_cache[channel.id] = wh
    return wh
