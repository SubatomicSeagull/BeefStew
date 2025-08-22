import discord
import re
import platform
import os
from beefutilities.TTS import ttsengine
from beefcommands.utilities.music_player.player_utils import handle_after_playing

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
            sanitised_text = sanitised_text.replace(match.group(0), {member.display_name})

    # replace role mentions
    for match in re.finditer(r"<@&(\d+)>", sanitised_text):
        role_id = int(match.group(1))
        role = ctx.guild.get_role(role_id)
        if role:
            sanitised_text = sanitised_text.replace(match.group(0), {role.name})
            
    # replace channel mentions
    for match in re.finditer(r"<#(\d+)>", sanitised_text):
        channel_id = int(match.group(1))
        channel = ctx.guild.get_channel(channel_id)
        if channel:
            sanitised_text = sanitised_text.replace(match.group(0), f"#{channel.name}")
    
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
    voice_client: discord.VoiceClient = ctx.guild.voice_client
    prev_content = None
    # check if the bot is connected to a voice channel
    if not voice_client or not voice_client.is_connected():
        print("Bot is not connected to a voice channel.")
        return
    
    message_text = await sanitise_output(ctx, message)
    
    if message_text is None or message_text.strip() == "":
        print("No valid text to speak.")
        return
    
    # dont return just beefstew
    if message_text == "beefstew.": return
    
    tts_file = ttsengine.generate_speech(message_text)
    
    if platform.system().lower() == "windows":
        exepath = os.getenv("FFMPEGEXE")
    else:
        exepath = "/usr/bin/ffmpeg"

    
    if voice_client.is_playing():
        prev_content = voice_client.source
        voice_client.pause()
        
    audio_source = discord.FFmpegPCMAudio(tts_file, executable=exepath)

    def after_playing(error):
        if error:
            print(f"Error during playback: {error}")
        else:
            print("Finished playing TTS message.")
        if os.path.exists(tts_file):
            os.remove(tts_file)
            print(f"Deleted temporary file: {tts_file}")
        if prev_content:
            voice_client.play(prev_content)
            print("Resumed previous audio.")

    
    
    voice_client.play(audio_source, after=lambda e: after_playing(e))

    return


