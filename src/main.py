import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from data import postgres


# Load the token from .env
try:
    load_dotenv()
except Exception as e:
    print("Dotenv load failed, either dotenv is not installed or there is no .env file.")
    postgres.log_error(e)

# Create client and intents objects
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)
kicked_members = set()
banned_members = set()


async def load_cogs():
    print("registering cogs...")
    await bot.load_extension("beefcmd.cogs.event_listener_cog")
    await bot.load_extension("beefcmd.cogs.incantations_cog")
    await bot.load_extension("beefcmd.cogs.invocations_cog")
    await bot.load_extension("beefcmd.cogs.moderation_cog")
    await bot.load_extension("beefcmd.cogs.utilities_cog")
    await bot.load_extension("beefcmd.cogs.visage_cog")

@bot.event
async def on_ready():
    print(f"Commands currently registered:")
    for command in bot.tree.get_commands():
        print(f"removing {command.name}")
        await bot.tree.remove_command(command.name)
    await load_cogs()
    await bot.tree.sync()
    print(f"{bot.user} is now online, may god help us all...")

# entrypoint
if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))
