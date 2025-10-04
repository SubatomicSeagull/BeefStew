import discord
from discord.ext import commands
import re
import platform
import os
from beefutilities.TTS import tts_engine
import asyncio

global _TTS_lock
_TTS_lock: bool = False

global g_Lock
g_Lock: bool = False

# set the global lock state
def get_lock_state_global():
    return g_Lock

# lock or unlock the tts globally
def set_lock_state_global(state: bool):
    global g_Lock
    g_Lock = state

# get the local lock state
def get_lock_state():
    return _TTS_lock
    
# lock or unlock the tts locally
def set_lock_state(state: bool):
    global _TTS_lock
    _TTS_lock = state

# remove unpronouncable characters from a message and make sure it ends with a .
async def sanitise_output(ctx, message):

    input_text = message
    sanitised_text = ""

    # if the input is a discord message object then just use the message content
    if isinstance(message, discord.Message):
        input_text = message.content

    # dont read out links
    if input_text.lower().startswith("http"):
        return

    print(f"Input text: {input_text}")
    sanitised_text = input_text

    # replace user id mentions with plaintext namesz
    for match in re.finditer(r"<@!?(\d+)>", sanitised_text):
        user_id = int(match.group(1))
        member = ctx.guild.get_member(user_id)
        if member:
            try:
                sanitised_text = sanitised_text.replace(match.group(0), str({member.display_name}))
            except Exception as e:
                print("Error replacing user mention: " + str(e))
                pass
            
    # replace role mentions
    for match in re.finditer(r"<@&(\d+)>", sanitised_text):
        role_id = int(match.group(1))
        role = ctx.guild.get_role(role_id)
        if role:
            try:
                sanitised_text = sanitised_text.replace(match.group(0), str({role.name}))
            except Exception as e:
                print("Error replacing role mention: " + str(e))
                pass
            
    # replace channel mentions
    for match in re.finditer(r"<#(\d+)>", sanitised_text):
        channel_id = int(match.group(1))
        channel = ctx.guild.get_channel(channel_id)
        if channel:
            try:
                sanitised_text = sanitised_text.replace(match.group(0), f"#{channel.name}")
            except Exception as e:
                print("Error replacing channel mention: " + str(e))
                pass
            
    # replace custom emojis with their names
    sanitised_text = re.sub(r"<a?:([a-zA-Z0-9_]+):\d+>", r"\1", sanitised_text)

    #clean unwanted symbols
    sanitised_text = re.sub(r"[^a-zA-Z0-9!\"£$%&;:'@.=+\- ]+", "", sanitised_text)

    # add a full stop at the end for smoother speech
    sanitised_text = sanitised_text.strip()
    if not sanitised_text.endswith("."):
        sanitised_text += "."

    print(f"Sanitised text: {sanitised_text}")
    return sanitised_text

async def speak_output(ctx, message):
    
    # initial params, check for local or global lock and the incoming context type
    if get_lock_state_global():
        print("GLOBAL LOCKED!!!!")
        return
    
    if get_lock_state():
        print("TTS LOCKED!!!!")
        return
    
    if isinstance(ctx, discord.Message) or isinstance(ctx, commands.Context):
        user = ctx.author

    elif isinstance(ctx, discord.Interaction):
        user = ctx.user
        

    loop = asyncio.get_event_loop()

    voice_client: discord.VoiceClient = ctx.guild.voice_client

    prev_content = None

    # check if the bot is connected to a voice channel
    if not voice_client or not voice_client.is_connected():
        if user.voice:
            from beefutilities.guilds import guild_voice_channel
            voice_client = await guild_voice_channel.join_vc(ctx.guild.voice_client, user)
            print(voice_client)
        else:
            print("=========================== TTS LOCK Off")
            set_lock_state(False)
            return
    
    # lock the tts while its procesing and speakingh
    print("=========================== TTS LOCK ON")
    set_lock_state(True)

    message_text = await sanitise_output(ctx, message)

    if message_text is None or message_text.strip() == "":
        print("No valid text to speak.")
        set_lock_state(False)
        return

    # dont return just beefstew
    if message_text == "beefstew." or message_text == ".": 
        set_lock_state(False)
        return
    
    tts_file = await tts_engine.generate_speech(message_text)

    if platform.system().lower() == "windows":
        exepath = os.getenv("FFMPEGEXE")
    else:
        exepath = "/usr/bin/ffmpeg"


    if voice_client.is_playing():
        prev_content = voice_client.source
        voice_client.pause()
        
    audio_source = discord.FFmpegPCMAudio(tts_file, pipe=True, executable=exepath)

    def after_playing(error):
        # try to close the bytes stream, sometimes doesnt work if it cant find the file or stream 
        try:
            print("closing tts bytes stream")
            tts_file.close()
        except Exception as e:
            print("didnt work..." + e)
            pass
        
        print("=========================== TTS LOCK OFF")
        set_lock_state(False)

        # if there was previous music, run /play to hook back into the queue loop and play the next audio after the resumed track has completed
        if prev_content:
            def retrace_prev_callback(error):
                print("callback from previous audio:")
            
                from beefcommands import music_player

                async def resume_music():
                    print("Running /play")
                    
                    # hacky fix coz sometimes the context gets overwritten
                    try: 
                        author = ctx.author
                    except AttributeError:
                        author = ctx.user
                    
                    await music_player.play(author, ctx.guild.voice_client, ctx.channel)
                    
                print("running resume_music in main loop")
                future = asyncio.run_coroutine_threadsafe(resume_music(), loop)
                try:
                    future.result(timeout=5)  # wait for it to complete or raise
                except Exception as e:
                    print("Exception in resume_music:", e)


            voice_client.play(prev_content, after = retrace_prev_callback)
            print("Resumed previous audio.")

    voice_client.play(audio_source, after=lambda e: after_playing(e))
    return
