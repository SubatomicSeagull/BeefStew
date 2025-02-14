import asyncio
import discord
import yt_dlp
import os
import platform
from beefcommands.utilities.music_player import queue
from beefutilities import voice_channel
from main import executor

async def play_next(ctx):
    # dont play anything if the bot isnt connected
    if not ctx.voice_client:
        return
    
    # retrive the queue
    queue_list = queue.get_queue()
    if queue.get_loop_flag() == True:
        
        # play the current_track link again and dont take from the queue
        current_track = queue.get_current_track()
        if current_track:
            await play_track(ctx, current_track[0], current_track[1])
            return
        
    # if the queue is not empty
    if queue_list:       
        # move the top of the queue to the currently playing
        current_track = queue_list.pop(0)
        queue.set_current_track(current_track)
        
        # play the song in currently_playing
        await play_track(ctx, queue.get_current_track_link(), queue.get_current_track_title())
    else:
        # start the disconnect timer
        disconnect_task = ctx.bot.loop.create_task(disconnect_timeout(ctx))
        ctx.bot.get_cog('MusicPlayerCog').disconnect_task = disconnect_task

async def handle_after_playing(ctx, error):
    # allow the voice handshake and ffmpeg process to settle
    await asyncio.sleep(1)
    
    # play the current_track link again and dont take from the queue
    if queue.get_loop_flag() == True:
        current_track = queue.get_current_track()
        if current_track:
            # play the some in currently playing
            await play_track(ctx, queue.get_current_track_link(), queue.get_current_track_title())
    else:
        await play_next(ctx)

async def play_track(ctx, url, title):
    # if the bot isnt in a voice channel, join it
    if not ctx.voice_client:
        await voice_channel.establish_voice_connection(ctx)
    
    # find the ffmpeg executable based on the OS
    if platform.system().lower() == "windows":
        exepath = os.getenv("FFMPEGEXE")
    else:
        exepath = "/usr/bin/ffmpeg"
    
    # define the audio options
    ydl_ops = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
        "key": "FFmpegExtractAudio",
        "preferredcodec": "opus",
        "preferredquality": "192"
    }
    
    try:
        # retrive the thread executor
        loop = asyncio.get_running_loop()
        
        # retrive the metadata for the youtube link and return the audio url
        
        metadata =  await loop.run_in_executor(executor, lambda: yt_dlp.YoutubeDL(ydl_ops).extract_info(url, download=False))
        audio_url = metadata["url"]   
    
    except Exception as e:
        await ctx.send(f"couldnt play {title} ({e})")
        return
    
    # define the source to play in discord voice client
    
    before_options=[
        "-nostdin",
        "-hide_banner",
        "-loglevel info",
        "-reconnect 1",
        "-reconnect_streamed 1",
        "-reconnect_delay_max 5"]
    
    options=[
        "-vn",
        "-ac 2",
        "-ar 48000",
        "-b:a 96k",
        "-bufsize 192k",
        "-maxrate 96k"
    ]
    
    source = discord.FFmpegOpusAudio(source=audio_url, executable=exepath, options=options, before_options=before_options)
    
    # define behaviour after playing a track
    def after_playing(error):
        if not ctx.voice_client:
            return
        
        if not queue.get_queue() and not queue.get_current_track():
            return
        
        if error:
            return
        
        # when playback ends, call the handler
        coro = handle_after_playing(ctx, error)
        future = asyncio.run_coroutine_threadsafe(coro, ctx.bot.loop)
        try:
            future.result()
        except:
            pass
        
    # play the song in the voice channel
    await ctx.send(f"Playing: **{title}**")
    ctx.voice_client.play(source, after=after_playing)


async def disconnect_timeout(ctx):
    try:
        # wait 5 minutes for another song to be queued
        await asyncio.sleep(300)
        if not queue.get_queue() and not ctx.voice_client.is_playing():
            await ctx.send("YAAAWNNN thers no more songs in the queue IM BORED!!! cya")
            await ctx.voice_client.disconnect()
    
    # interupt the timer when the queue is no longer empty
    except asyncio.CancelledError:
        pass