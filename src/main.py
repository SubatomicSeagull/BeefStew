import os
import sys
from dotenv import load_dotenv
import discord
from discord.ext import commands
from beefcommands.events import message_events
from data import postgres
import asyncio
from concurrent.futures import ThreadPoolExecutor
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from trello import TrelloClient
from beefutilities.TTS import speak


# instantiate the thread pool executor
executor = ThreadPoolExecutor(max_workers=4)

# start up the multithreading loop
asyncloop = asyncio.new_event_loop()
asyncio.set_event_loop(asyncloop)

# load the token from .env
try:
    load_dotenv()
except Exception as e:
    print("Dotenv load failed, either dotenv is not installed or there is no .env file.")
    postgres.log_error(e)

# log in to the spotify api
sp_client = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv("SPOTIFYCLIENTID"), client_secret=os.getenv("SPOTIFYCLIENTSECRET")))

trello_client = TrelloClient(api_key=(os.getenv("TRELLOAPIKEY")), api_secret=(os.getenv("TRELLOAPISECRET")), token=(os.getenv("TRELLOTOKEN")))

# create client and intents objects
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)
speak.init(bot)
message_events.init(bot)

kicked_members = set()
banned_members = set()
# load the commands though the cogs
async def load_cogs():
    print("> registering cogs...")
    await bot.load_extension("beefcommands.cogs.event_listener_cog")
    await bot.load_extension("beefcommands.cogs.incantations_cog")
    await bot.load_extension("beefcommands.cogs.invocations_cog")
    await bot.load_extension("beefcommands.cogs.moderation_cog")
    await bot.load_extension("beefcommands.cogs.utilities_cog")
    await bot.load_extension("beefcommands.cogs.visage_cog")
    await bot.load_extension("beefcommands.cogs.music_player_cog")
    await bot.load_extension("beefcommands.cogs.task_scheduler_cog")


@bot.event
async def on_ready():   
    bot.loop_ref = asyncio.get_running_loop() 
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="you..."))
        
    # load the cogs 
    await load_cogs()

    # re-register all the command
    await bot.tree.sync()
    
    # go!
    print(f"> \033[1;91m{bot.user} is now online, may god help us all...\033[0m")

# entrypoint
if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))
