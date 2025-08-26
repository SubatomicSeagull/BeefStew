import asyncio

async def join_vc(voice_client, user):
    
    # if the bot isnt already in a channel, connect
    if not voice_client:
        await user.voice.channel.connect()

    # move voice channels if it doesnt match the users vc
    elif voice_client.channel != user.voice.channel:
        await voice_client.move_to(user.voice.channel)
    else:
        return
    
async def leave_vc(voice_client):
    # if a voice connection is established, disconnect
    if voice_client:
        await voice_client.disconnect()

    # give time for the ffmpeg process and voice handshake to shut down
    await asyncio.sleep(2)

    return