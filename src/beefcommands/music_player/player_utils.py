import asyncio
import os
import platform
from beefcommands.music_player import queue
import discord
import yt_dlp
from main import bot #<- badddd


async def play_next(voice_client, tx_channel):
    # dont play anything if the bot isnt connected
    if not voice_client:
        return
    
    # retrive the queue
    queue_list = queue.get_queue()
    if queue.get_loop_flag() == True:
        
        # play the current_track link again and dont take from the queue
        current_track = queue.get_current_track()
        if current_track:
            await play_track(voice_client, tx_channel, current_track[0], current_track[1])
            return
        
    # if the queue is not empty
    if queue_list:       
        # move the top of the queue to the currently playing
        current_track = queue_list.pop(0)
        queue.set_current_track(current_track)
        
        # play the song in currently_playing
        await play_track(voice_client, tx_channel, queue.get_current_track_link(), queue.get_current_track_title())
    
    else:
        try:
            # wait 5 minutes for another song to be queued
            await asyncio.sleep(300)
            if not queue.get_queue() and not voice_client.is_playing():
                await voice_client.disconnect()
    # interupt the timer when the queue is no longer empty
        except asyncio.CancelledError:
            pass

async def handle_after_playing(voice_client, tx_channel, error):
    if not voice_client:
        return
    
    if not queue.get_queue() and not queue.get_current_track():
        return
    
    if error:
        return
    
    # allow the voice handshake and ffmpeg process to settle
    await asyncio.sleep(1)
    
    # play the current_track link again and dont take from the queue
    if queue.get_loop_flag() == True:
        current_track = queue.get_current_track()
        if current_track:
            # play the some in currently playing
            await play_track(voice_client, tx_channel, queue.get_current_track_link(), queue.get_current_track_title())
    else:
        await play_next(voice_client,tx_channel)

async def play_track(voice_client, tx_channel, url, title):
    
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
        print("retrieving event loop")
        loop = asyncio.get_running_loop()
        
        # retrive the metadata for the youtube link and return the audio url
        print(f"retrieving metadata for {title}")
        metadata =  await loop.run_in_executor(bot.executor, lambda: yt_dlp.YoutubeDL(ydl_ops).extract_info(url, download=False))
        audio_url = metadata["url"]   
    
    except Exception as e:
        await tx_channel.send(f"Couldn't play {title} ({e})")
        return
    
    # define the source to play in discord voice client
    before_options=[
        "-nostdin",
        "-hide_banner",
        "-loglevel info",
        "-reconnect 1",
        "-reconnect_at_eof 1",
        "-reconnect_on_network_error 1",
        "-reconnect_streamed 1",
        "-reconnect_delay_max 5"]
    
    options=[
        "-vn",
        "-ac 2",
        "-ar 48000",
        "-b:a 96k",
        "-bufsize 192k",
        "-maxrate 96k",
        " -rw_timeout 10000000"
    ]
    
    source = discord.FFmpegOpusAudio(source=audio_url, executable=exepath, options=options, before_options=before_options)

    # define behaviour after playing a track
    def after_playing(error, loop):
        # use the current bot loop for thread safety
        if loop and loop.is_running():
            # schedule the coroutine in the running loop
            future = asyncio.run_coroutine_threadsafe(
                handle_after_playing(voice_client, tx_channel, error), loop
            )
            future.result()
        else:
            print("No running event loop; cannot schedule after_playing task.")
            pass

    # play the song in the voice channel
    await tx_channel.send(f"Playing: **{title}**")
    voice_client.play(source, after=lambda e: after_playing(e, loop))

