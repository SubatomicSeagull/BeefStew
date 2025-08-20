import discord
import re
import platform
import os
from beefutilities.TTS import ttsengine

async def sanitise_output(ctx, message):
    
    decorator = re.compile(r"<(@!?|@&|#)\d+>")
    
    input_text = message
    sanitised_text = ""
    
    # if the input is a discord message object then just use the message content
    if isinstance(message, discord.Message):
        input_text = message.content
    
    print(f"Input text: {input_text}")
    
    # if no discord decorators, return the text
    if not decorator.search(input_text):
        return input_text
    
    # replace user id mentions with plaintext namesz
    for match in re.finditer(r"<@!?(\d+)>", input_text):
        user_id = int(match.group(1))
        member = ctx.guild.get_member(user_id)
        if member:
            sanitised_text = input_text.replace(match.group(0), {member.display_name})

    # replace role mentions
    for match in re.finditer(r"<@&(\d+)>", input_text):
        role_id = int(match.group(1))
        role = ctx.guild.get_role(role_id)
        if role:
            sanitised_text = input_text.replace(match.group(0), {role.name})
            
    # replace channel mentions
    for match in re.finditer(r"<#(\d+)>", input_text):
        channel_id = int(match.group(1))
        channel = ctx.guild.get_channel(channel_id)
        if channel:
            sanitised_text = input_text.replace(match.group(0), f"#{channel.name}")
    
    print(f"Sanitised text: {sanitised_text}")
    return sanitised_text

async def speak(message: discord.Message):
    if not message.author.voice:
        print("User is not in a voice channel.")
        return
    
    voice_client: discord.VoiceClient = message.guild.voice_client
    
    if not voice_client or not voice_client.is_connected():
        print("Bot is not connected to a voice channel.")
        return
    
    channel = message.author.voice.channel
    message_text = await sanitise_output(message)
    
    tts_file = ttsengine.generate_speech(message_text)
    
    if platform.system().lower() == "windows":
        exepath = os.getenv("FFMPEGEXE")
    else:
        exepath = "/usr/bin/ffmpeg"

        
    audio_source = discord.FFmpegPCMAudio(tts_file, executable=exepath)



    def after_playing(error):
        if error:
            print(f"Error during playback: {error}")
        else:
            print("Finished playing TTS message.")
        if os.path.exists(tts_file):
            os.remove(tts_file)
            print(f"Deleted temporary file: {tts_file}")


    print(f"Playing TTS in {channel.name} for {message.author.display_name}")
    voice_client.play(audio_source, after=lambda e: after_playing(e))

    return


