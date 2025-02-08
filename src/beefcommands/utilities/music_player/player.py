from beefutilities import voice_channel
from beefcommands.utilities.music_player import queue
from beefcommands.utilities.music_player.player_utils import play_next

async def play(ctx, *args):
    if not ctx.author.voice:
        await ctx.reply("ur not in a vc")
        return
    
    url = " ".join(args)
    if url:
        await queue.handle_queue(ctx, url, insert=True)
        print("establishing voice connection")
        await voice_channel.establish_voice_connection(ctx)
        print("playing next")
    
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