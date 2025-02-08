import discord
import os
import asyncio
import yt_dlp
from beefutilities import voice_channel
from beefcommands.utilities.music_player import player
from beefcommands.utilities.music_player import queue
from beefcommands.cogs.music_player_cog import MusicPlayerCog
from main import executor


async def play(ctx, *args):
    if not ctx.author.voice:
            await ctx.reply("ur not in a vc")
            return
        
    url = " ".join(args)
    if url:
        await queue.handle_queue(ctx, url, insert=True)
        print("establishing voice connection")
        await voice_channel.establish_voice_connection(ctx)
        print("playing next")
    
    if not (ctx.voice_client and ctx.voice_client.is_playing()):
        await player.play_next(ctx)

async def pause(ctx):
    if not ctx.voice_client or not ctx.voice_client.is_playing():
        return
    ctx.voice_client.pause()
    
async def resume(ctx):
    if not ctx.voice_client or not ctx.voice_client.is_paused():
        return
    ctx.voice_client.resume()

async def play_track(ctx, url, title):
        if not ctx.voice_client:
            await voice_channel.establish_voice_connection(ctx)
        exepath = os.getenv("FFMPEGEXE")
        MusicPlayerCog.get_current_track_info = (url, title)
        ydl_ops = {
            "format": "bestaudio/best",
            "noplaylist": True,
            "quiet": True,
        }
        
        try:
            loop = asyncio.get_running_loop()
            metadata =  await loop.run_in_executor(executor, lambda: yt_dlp.YoutubeDL(ydl_ops).extract_info(url, download=False))
            audio_url = metadata["url"]   
        except Exception as e:
            await ctx.send(f"couldnt play {title} ({e})")
            return
        
        source = discord.FFmpegPCMAudio(source=audio_url, executable=exepath)
        
        def after_playing(error):
            if error:
                print(f"An error occurred: {error}")
                return
            
            # When playback ends, call the handler.
            coro = handle_after_playing(ctx, error)
            future = asyncio.run_coroutine_threadsafe(coro, MusicPlayerCog.bot.loop)
            try:
                future.result()
            except:
                pass
            
        ctx.voice_client.play(source, after=after_playing)
        await ctx.send(f"Playing: **{title}**")
        
async def play_next(ctx):
    print("song done! playing next")
    queue = queue.get_queue()
    
    if queue.get_loop_flag() == True:
        print("loop flag true")
        current_track = queue.get_current_track()
        if current_track:
            await play_track(ctx, current_track[0], current_track[1])
            return
        
    if queue:
        current_track = queue.pop(0)
        queue.set_current_track(current_track)
        await play_track(ctx, current_track[0], current_track[1])
    else:
        MusicPlayerCog.disconnect_task = MusicPlayerCog.bot.loop.create_task(disconnect_timeout(ctx))
                
async def handle_after_playing(ctx, error):
    if queue.get_loop_flag() == True:
        print("loop flag true")
        current_track = queue.get_current_track()
        if current_track:
            await play_track(ctx, queue.get_current_track_link(), queue.get_current_track_title())
    else:
        await play_next(ctx)
        
        
async def skip(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        
async def disconnect_timeout(ctx):
    try:
        print("no songs in the queue, waiting for 5 mintues")
        await asyncio.sleep(300)
        if not queue.get_queue():
            await ctx.send("YAAAWNNN thers no more songs in the queue IM BORED!!! cya")
            await ctx.voice_client.disconnect()
    except asyncio.CancelledError:
        print("new song queued, disconnect cancelled")