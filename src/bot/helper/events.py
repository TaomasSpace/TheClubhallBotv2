from bot_instance import bot
from Database.databaseHelper import get_custom_role, delete_custom_role
import discord
import os
from Database.initializeDB import init_db
import helper.helper
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=".env")

WELCOME_CHANNEL_ID = os.getenv("WELCOME_CHANNEL_ID")
EXIT_CHANNEL_ID = os.getenv("EXIT_CHANNEL_ID")
BOOSTER_CHANNEL_ID = os.getenv("BOOSTER_CHANNEL_ID")

# Event: Bot is ready
@bot.event
async def on_ready():
    init_db()
    await bot.tree.sync()  # Ensure slash commands are registered
    print(f"Bot is online as {bot.user}")
    print("Guilds:", bot.guilds)

# Event: Member updates (e.g. starts or stops boosting)
@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    # User stopped boosting → delete their custom role
    if before.premium_since and not after.premium_since:
        role_id = get_custom_role(str(after.id))
        if role_id:
            role = after.guild.get_role(role_id)
            if role:
                try:
                    await role.delete(reason="User stopped boosting")
                except:
                    pass  # Silently ignore if bot lacks permissions
            delete_custom_role(str(after.id))

    # User started boosting → send thank-you message
    if not before.premium_since and after.premium_since:
        channel = bot.get_channel(BOOSTER_CHANNEL_ID)
        if channel:
            await channel.send(
                f"🎉 {after.mention} just boosted the server — thank you so much for the support! 💜\n"
                f"<@!756537363509018736> will update your booster level soon.\n"
                f"Check <https://discord.com/channels/1351475070312255498/1351528109702119496/1371189412125216869> to see what new features you unlock!"
            )

# Event: New member joins → assign role and send welcome message
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Member")
    if role:
        await member.add_roles(role)

    channel = bot.get_channel(int(WELCOME_CHANNEL_ID))
    if channel:
        server_name = member.guild.name
        member_count = member.guild.member_count
        message = (
            f"Welcome new member {member.mention}! <3\n"
            f"Thanks for joining **{server_name}**.\n"
            f"Don't forget to read the #rules and #information!\n"
            f"We are now **{member_count}** members."
        )
        await channel.send(message)

# Event: Member leaves → send exit message
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(int(EXIT_CHANNEL_ID))
    if channel:
        member_count = member.guild.member_count
        message = f"It seems {member.name} has left us... We are now **{member_count}** members."
        await channel.send(message)

# Event: On every new message
@bot.event
async def on_message(message: discord.Message):
    # Ignore bot/webhook messages
    if message.author.bot or message.webhook_id:
        return

    # Forced lowercase handling
    if message.author.id in helper.helper.lowercase_locked:
        try:
            await message.delete()
        except discord.Forbidden:
            return
        wh = await helper.get_channel_webhook(message.channel)
        await wh.send(
            content=message.content.lower(),
            username=message.author.display_name,
            avatar_url=message.author.display_avatar.url,
            allowed_mentions=discord.AllowedMentions.all(),
        )

    # Trigger response check (basic keyword-response system)
    content = message.content.lower()
    for trigger, reply in helper.TRIGGER_RESPONSES.items():
        if trigger.lower() in content:
            await message.channel.send(reply)
            break

    # Ensure command processing still works
    await bot.process_commands(message)
