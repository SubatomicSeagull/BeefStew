from beefutilities import voice_channel
from beefcommands.utilities.music_player import queue
from beefcommands.utilities.music_player.player_utils import play_next

async def play(ctx, *args):
    #dont run if the user isnt in a voice channel
    if not ctx.author.voice:
        await ctx.reply("ur not in a vc")
        return
    
    #join together arbitrary arguments into search query
    url = " ".join(args)
    if url:
        # add the item to the front of the queue
        await queue.handle_queue(ctx, url, insert=True)
        # join the voice channel if its not in there already
        await voice_channel.establish_voice_connection(ctx)
    
    # start playing the queue
    if not (ctx.voice_client and ctx.voice_client.is_playing()):
        await play_next(ctx)

async def pause(ctx):
    if not ctx.voice_client or not ctx.voice_client.is_playing():
        return
    ctx.voice_client.pause()
    
async def resume(ctx):
    if not ctx.voice_client or not ctx.voice_client.is_paused():
        return
    ctx.voice_client.resume()

async def skip(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()