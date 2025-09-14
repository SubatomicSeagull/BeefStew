import discord
from beefutilities.guilds import guild_voice_channel
from beefcommands.music_player import queue, player_utils


async def play(user: discord.Member, voice_client, tx_channel, *args):
    # don't run if the user isn't in a voice channel
    if not user.voice:
        return

    voice_client = user.voice.channel.guild.voice_client

    # join together arbitrary arguments into search query
    url = " ".join(args).strip()
    if url:
        print("joining vc")
        voice_client = await guild_voice_channel.join_vc(voice_client, user)

        print(f"**{user.name}** requested **{url}**")
        await queue.handle_queue(user, tx_channel, url, insert = True)

    if voice_client and not voice_client.is_playing():
        await player_utils.play_next(voice_client, tx_channel)

async def pause(voice_client):
    if not voice_client or not voice_client.is_playing():
        return
    voice_client.pause()

async def resume(voice_client):
    if not voice_client or not voice_client.is_paused():
        return
    voice_client.resume()

async def skip(voice_client):
    if voice_client.is_playing():
        voice_client.stop()