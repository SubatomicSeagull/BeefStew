import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from data import postgres
import yt_dlp


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

@bot.command(name="join")
async def join(ctx, url):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        
        #path = (os.path.join((os.path.dirname(os.path.abspath(__file__))), "assets", "media","song.mp3"))
        exepath = "C:\\Users\\jamie\\Desktop\\ffmpeg-2025-01-13-git-851a84650e-full_build\\bin\\ffmpeg.exe"
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
        }
    
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            print(info_dict)
            audio_url = info_dict["url"]
        
        await ctx.send(f"playing {info_dict['title']}")
        source = discord.FFmpegPCMAudio(source=audio_url, executable=exepath)
        
        def after_playing(error):
            # Disconnect the bot after playing
            if error:
                print(f"An error occurred: {error}")
            coro = ctx.voice_client.disconnect()
            bot.loop.create_task(coro)
            
        ctx.voice_client.play(source, after=after_playing)

# entrypoint
if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))
