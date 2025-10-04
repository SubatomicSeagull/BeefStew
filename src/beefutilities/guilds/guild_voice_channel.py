import asyncio
from beefcommands import music_player
from beefutilities.TTS.speak import set_lock_state

async def join_vc(voice_client, user):
    # if the bot isn't already in a channel, connect
    if not voice_client:
        return await user.voice.channel.connect()

    # move voice channels if it doesn't match the user's vc
    elif voice_client.channel != user.voice.channel:
        await voice_client.move_to(user.voice.channel)
        return voice_client

    return voice_client

async def leave_vc(voice_client):
    print("lock off")
    set_lock_state(False)
    # if a voice connection is established, disconnect
    if voice_client:
        await music_player.clear()
        await voice_client.disconnect()

    # give time for the ffmpeg process and voice handshake to shut down
    await asyncio.sleep(2)

    return