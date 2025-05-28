import discord
from Database.databaseHelper import register_user, get_stats
import configparser
from pathlib import Path

CONFIG_PATH = Path(__file__).parents[3] / "config.ini"
config = configparser.ConfigParser()
config.optionxform = str  # nur relevant bei keys mit Groß-/Kleinschreibung
if CONFIG_PATH.is_file():
    config.read(CONFIG_PATH)

STAT_NAMES = [
    stat.strip().lower() for stat in config["Gameconfigs"]["STAT_NAMES"].split(",")
]


async def stats(interaction: discord.Interaction, user: discord.Member | None = None):
    target = user or interaction.user
    register_user(str(target.id), target.display_name)
    stats = get_stats(str(target.id))
    description = "\n".join(f"**{s.title()}**: {stats[s]}" for s in STAT_NAMES)
    embed = discord.Embed(
        title=f"{target.display_name}'s Stats",
        description=description,
        colour=discord.Colour.green(),
    )
    embed.set_footer(text=f"Unspent points: {stats['stat_points']}")
    await interaction.response.send_message(embed=embed, ephemeral=(user is None))
