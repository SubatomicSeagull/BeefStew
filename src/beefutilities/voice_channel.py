from beefcommands.utilities.music_player import player
from beefcommands.utilities.music_player import queue

async def join_vc(ctx):
    # check to see if the user is ina voice channel
    if not ctx.author.voice:
        await ctx.reply("ur not in a vc")
        return
    
    # if the bot isnt already in a channel, connect
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()
        
        # automatically start playing the queue
        await player.play_next(ctx)
        
    # move voice channels if it doesnt match the users vc
    elif ctx.voice_client.channel != ctx.author.voice.channel:
        await ctx.voice_client.move_to(ctx.author.voice.channel)
        await player.play_next(ctx)
    else:
        return
    
async def leave_vc(ctx):
    # if a voice connection is established, disconnect
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        
        # clear the queue
        queue.clear_queue()
        
        # clear the current track
        queue.clear_current_track()
        
async def establish_voice_connection(ctx):
    # if the bot isnt already in a voice channel, connect
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()
        
    # move voice channels if it doesnt match the users vc
    elif ctx.voice_client.channel != ctx.author.voice.channel:
        await ctx.voice_client.move_to(ctx.author.voice.channel)