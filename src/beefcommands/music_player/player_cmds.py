from beefutilities.guilds import guild_voice_channel
from beefcommands.music_player import queue, player_utils


async def play(user, voice_client, tx_channel, *args):
    #dont run if the user isnt in a voice channel
    if not user.voice:
        return
    
    #join together arbitrary arguments into search query
    url = " ".join(args)
    print(url)
    if url and url != "  ":
        print(f"**{user.name}** requested **{url}**")
        # add the item to the front of the queue
        await queue.handle_queue(user, tx_channel, url, insert=True)
        
        # join the voice channel if its not in there already
        await guild_voice_channel.join_vc(voice_client, user)
    
    # start playing the queue
    if (voice_client and not voice_client.is_playing()):
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