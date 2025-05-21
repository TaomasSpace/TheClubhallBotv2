import discord
from Database.databaseHelper import get_money, set_money
from discord import ui
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=".env")
BOT_USERID = os.getenv("BOT_USERID")

# Checks if a Discord member has a specific role by name
def has_role(member: discord.Member, role_name: str):
    return any(role.name == role_name for role in member.roles)

# Trigger-based auto-reply map (case-sensitive, evaluated manually)
TRIGGER_RESPONSES = {
    "シャドウストーム": "Our beautiful majestic Emperor シャドウストーム! Long live our beloved King 👑",
    "goodyb": "Our beautiful majestic Emperor goodyb! Long live our beloved King 👑",
    "Taoma": "Our beautiful majestic Emperor TAOMA™! Long live our beloved King 👑",
}

# Users whose messages will be force-converted to lowercase
lowercase_locked: set[int] = set()

# Webhook cache for reuse across messages
webhook_cache: dict[int, discord.Webhook] = {}

# Retrieves or creates a reusable webhook for a given text channel
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

# Safely adds coins to a user's balance, respecting the server's (bank) balance limit
def safe_add_coins(user_id: str, amount: int) -> int:
    if amount <= 0:
        return 0

    bank_balance = get_money(BOT_USERID)
    if bank_balance <= 0:
        return 0

    addable = min(amount, bank_balance)

    # Deduct from bank and credit user
    set_money(BOT_USERID, bank_balance - addable)
    old_balance = get_money(user_id)
    set_money(user_id, old_balance + addable)

    return addable

# UI component for accepting or declining a coin transfer request
class RequestView(ui.View):
    def __init__(self, sender_id, receiver_id, amount):
        super().__init__(timeout=60)
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount

    @ui.button(label="Accept", style=discord.ButtonStyle.success)
    async def accept(self, interaction: discord.Interaction, button: ui.Button):
        # Only the target user can accept the request
        if interaction.user.id != self.receiver_id:
            await interaction.response.send_message(
                "This request isn't for you.", ephemeral=True
            )
            return

        sender_balance = get_money(str(self.sender_id))
        receiver_balance = get_money(str(self.receiver_id))

        if receiver_balance < self.amount:
            await interaction.response.send_message(
                "You don't have enough clubhall coins to accept this request.",
                ephemeral=True,
            )
            return

        # Execute coin transfer
        set_money(str(self.receiver_id), receiver_balance - self.amount)
        set_money(str(self.sender_id), sender_balance + self.amount)

        await interaction.response.edit_message(
            content=f"✅ Request accepted. {self.amount} clubhall coins sent!",
            view=None,
        )

    @ui.button(label="Decline", style=discord.ButtonStyle.danger)
    async def decline(self, interaction: discord.Interaction, button: ui.Button):
        # Only the target user can decline the request
        if interaction.user.id != self.receiver_id:
            await interaction.response.send_message(
                "This request isn't for you.", ephemeral=True
            )
            return

        await interaction.response.edit_message(
            content="❌ Request declined.", view=None
        )
