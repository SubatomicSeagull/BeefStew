import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from trello import TrelloClient
from beefcommands.invocations.joker_score.sacred_words import (
    load_sacred_words,
    clear_sacred_words,
)

# -------------------------
# ENV
# -------------------------
try:
    load_dotenv()
except Exception:
    print("Dotenv load failed, either dotenv is not installed or there is no .env file.")

sp_client = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=os.getenv("SPOTIFYCLIENTID"),client_secret=os.getenv("SPOTIFYCLIENTSECRET"),))

trello_client = TrelloClient(
api_key=os.getenv("TRELLOAPIKEY"),api_secret=os.getenv("TRELLOAPISECRET"),token=os.getenv("TRELLOTOKEN"),)

bot_loop: asyncio.AbstractEventLoop | None = None

class BeefStew(commands.Bot):
    async def setup_hook(self):
        global bot_loop
        bot_loop = asyncio.get_running_loop()
        print("> bot event loop captured")

        # load cogs
        await self.load_all_cogs()

        # sync commands
        await self.tree.sync()

        load_sacred_words()

        print("> setup complete")

    async def load_all_cogs(self):
        print("> registering cogs…")
        base = os.path.join("src", "beefcommands", "cogs")
        for filename in os.listdir(base):
            if not filename.endswith(".py"):
                continue
            # visage context menu is set up as an extention of the visage cog
            if filename == "visage_context_menu.py":
                continue
            ext = f"beefcommands.cogs.{filename[:-3]}"
            await self.load_extension(ext)


intents = discord.Intents.all()
intents.message_content = True

bot = BeefStew(command_prefix="/", intents=intents)

# executor for blocking APIs (Spotify, Trello, etc)
bot.executor = ThreadPoolExecutor(max_workers=4)

kicked_members = set()
banned_members = set()

# -------------------------
# Events
# -------------------------
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online,activity=discord.Activity(type=discord.ActivityType.watching,name="you...",),)
    print(f"> \033[1;91m{bot.user} is now online, may god help us all...\033[0m")


@bot.check
async def globally_block_dms(ctx):
    return ctx.guild is not None


async def _guild_only_interaction_check(interaction: discord.Interaction) -> bool:
    if interaction.guild is None:
        await interaction.response.send_message("NO DMS GRRR", ephemeral=True)
        return False
    return True
bot.tree.interaction_check = _guild_only_interaction_check


# entrypoint
if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))