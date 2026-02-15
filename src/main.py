import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import asyncio
from concurrent.futures import ThreadPoolExecutor
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import threading
from trello import TrelloClient
from beefcommands.invocations.joker_score.sacred_words import load_sacred_words, clear_sacred_words

# start up the multithreading loop
asyncloop = asyncio.new_event_loop()
asyncio.set_event_loop(asyncloop)

# load the token from .env
try:
    load_dotenv()
except Exception as e:
    print("Dotenv load failed, either dotenv is not installed or there is no .env file.")

# log in to the spotify api
sp_client = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv("SPOTIFYCLIENTID"), client_secret = os.getenv("SPOTIFYCLIENTSECRET")))

# log in to the trello api
trello_client = TrelloClient(api_key = (os.getenv("TRELLOAPIKEY")), api_secret=(os.getenv("TRELLOAPISECRET")), token=(os.getenv("TRELLOTOKEN")))

# create client and intents objects
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# define the executor as an extension of the bot
bot.executor = ThreadPoolExecutor(max_workers = 4)

kicked_members = set()
banned_members = set()

# cogs to be loaded
cogs = (
    "beefcommands.cogs.event_listener_cog",
    "beefcommands.cogs.incantations_cog",
    "beefcommands.cogs.invocations_cog",
    "beefcommands.cogs.moderation_cog",
    "beefcommands.cogs.utilities_cog",
    "beefcommands.cogs.visage_cog",
    "beefcommands.cogs.music_player_cog",
    "beefcommands.cogs.task_scheduler_cog"
)

# load the commands through the cogs
async def load_cogs():
    print("> registering cogs...")
    for cog in cogs:
        await bot.load_extension(cog)

@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.online, activity = discord.Activity(type = discord.ActivityType.watching, name = "you..."))

    # load the cogs
    await load_cogs()

    # re-register all the commands
    await bot.tree.sync()

    # generate new saint and sinner word for the day
    load_sacred_words()

    
    # go!
    print(f"> \033[1;91m{bot.user} is now online, may god help us all...\033[0m")
    

# blocking prefix commands in DMs
@bot.check
async def globally_block_dms(ctx):
    return ctx.guild is not None

# blocking slash and context commands in DMs
async def _guild_only_interaction_check(interaction: discord.Interaction) -> bool:
    if interaction.guild is None:
        await interaction.response.send_message("you can only use commands in the server, nothing private between friends", ephemeral = True)
        return False
    return True

bot.tree.interaction_check = _guild_only_interaction_check

# entrypoint
if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))
