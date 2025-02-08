import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from data import postgres
import yt_dlp
import asyncio
from concurrent.futures import ThreadPoolExecutor
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

executor = ThreadPoolExecutor(max_workers=4)
asyncloop = asyncio.new_event_loop()
asyncio.set_event_loop(asyncloop)
sp_client = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv("SPOTIFYCLIENTID"), client_secret=os.getenv("SPOTIFYCLIENTSECRET")))

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
    await bot.load_extension("beefcommands.cogs.event_listener_cog")
    await bot.load_extension("beefcommands.cogs.incantations_cog")
    await bot.load_extension("beefcommands.cogs.invocations_cog")
    await bot.load_extension("beefcommands.cogs.moderation_cog")
    await bot.load_extension("beefcommands.cogs.utilities_cog")
    await bot.load_extension("beefcommands.cogs.visage_cog")
    await bot.load_extension("beefcommands.cogs.music_player_cog")

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
