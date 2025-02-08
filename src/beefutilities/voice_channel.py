from beefcommands.utilities.music_player import player
from beefcommands.utilities.music_player import queue

async def join_vc(ctx):
    if not ctx.author.voice:
        await ctx.reply("ur not in a vc")
        return
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()
        await player.play_next(ctx)
    elif ctx.voice_client.channel != ctx.author.voice.channel:
        await ctx.voice_client.move_to(ctx.author.voice.channel)
        await player.play_next(ctx)
    else:
        return
    
async def leave_vc(ctx):
    print("leaving vc")
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        print("clearing the queue")
        queue.clear_queue()
        print("stopping the current track")
        queue.clear_current_track()
        
async def establish_voice_connection(ctx):
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()
    elif ctx.voice_client.channel != ctx.author.voice.channel:
        await ctx.voice_client.move_to(ctx.author.voice.channel)