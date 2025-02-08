import asyncio
import discord
import yt_dlp
import os
from beefcommands.utilities.music_player import queue
from beefutilities import voice_channel
from main import executor

async def play_next(ctx):
    print("song done! playing next")
    queue_list = queue.get_queue()
    
    if queue.get_loop_flag() == True:
        print("loop flag true")
        current_track = queue.get_current_track()
        if current_track:
            await play_track(ctx, current_track[0], current_track[1])
            return
        
    if queue_list:
        current_track = queue_list.pop(0)
        queue.set_current_track(current_track)
        await play_track(ctx, current_track[0], current_track[1])
    else:
        disconnect_task = ctx.bot.loop.create_task(disconnect_timeout(ctx))
        ctx.bot.get_cog('MusicPlayerCog').disconnect_task = disconnect_task

async def handle_after_playing(ctx, error):
    if queue.get_loop_flag() == True:
        print("loop flag true")
        current_track = queue.get_current_track()
        if current_track:
            await play_track(ctx, queue.get_current_track_link(), queue.get_current_track_title())
    else:
        await play_next(ctx)

async def play_track(ctx, url, title):
    if not ctx.voice_client:
        await voice_channel.establish_voice_connection(ctx)
    exepath = os.getenv("FFMPEGEXE")
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
        future = asyncio.run_coroutine_threadsafe(coro, ctx.bot.loop)
        try:
            future.result()
        except:
            pass
        
    ctx.voice_client.play(source, after=after_playing)
    await ctx.send(f"Playing: **{title}**")

async def disconnect_timeout(ctx):
    try:
        print("no songs in the queue, waiting for 5 mintues")
        await asyncio.sleep(300)
        if not queue.get_queue():
            await ctx.send("YAAAWNNN thers no more songs in the queue IM BORED!!! cya")
            await ctx.voice_client.disconnect()
    except asyncio.CancelledError:
        print("new song queued, disconnect cancelled")