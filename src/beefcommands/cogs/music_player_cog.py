import asyncio
from discord.ext import commands
from beefutilities import voice_channel
from beefcommands.utilities.music_player import player
from beefcommands.utilities.music_player import queue

class MusicPlayerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.disconnect_task = None
    
    # cancel disconnect timer
    def cancel_disconnect_time(self):
        if self.disconnect_task and not self.disconnect_task.done():
            self.disconnect_task.cancel()
            self.disconnect_task = None    
    
    # join the channel and play the queue if its populated
    @commands.command(name="join", description="get in here!!")
    async def mp_join_vc(self, ctx):
        await voice_channel.join_vc(ctx)
    
    # leave the channel and clear the queue
    @commands.command(name="leave", aliases=["fuckoff"],  description="fukoff")
    async def mp_leave_vc(self, ctx):
        await voice_channel.leave_vc(ctx)

    # play the given song at the front of the queue, or just play the queue if no query
    @commands.command(name="play", aliases=["p"], description="play the funky music white boy")
    async def mp_play(self, ctx, *args):
        await player.play(ctx, *args)

    # pause playback
    @commands.command(name="pause", description="Pauses the current track")
    async def mp_pause(self, ctx):
        await player.pause(ctx)

    # resume playback
    @commands.command(name="resume", description="Resumes the paused track")
    async def mp_resume(self, ctx):
        await player.resume(ctx)
    
    # skip to next song in the queue
    @commands.command(name="skip", aliases=["next"], description="next pleaes")
    async def mp_skip(self, ctx):
        await player.skip(ctx)
    
    # add query to the back of the queue
    @commands.command(name="queue", aliases=["q"], description="add something to the back of the queue")
    async def mp_queue(self, ctx, *args):
        await queue.qadd(ctx, *args)
    
    # print the queue
    @commands.command(name="queuelist", aliases=["qlist", "list", "queue_list", "listqueue", "list_queue"], description="lists the queue")
    async def mp_queue_list(self, ctx):
        await queue.qlist(ctx)
         
    # clear the queue
    @commands.command(name="queueclear", aliases=["qclear", "clear", "queue_clear", "clear_queue"])
    async def mp_queue_clear(self, ctx):
        await queue.qclear(ctx)
        
    # shuffle the queue
    @commands.command(name="shuffle", description="shuffle the queue")
    async def mp_queue_shuffle(self, ctx):
        await queue.qshuffle(ctx)
    
    # toggle loop
    @commands.command(name="loop", aliases=["repeat"], description="loop the current song")
    async def mp_loop_queue(self, ctx):
        await queue.qloop(ctx)

# cog startup
async def setup(bot):
    print("- music player cog setup")
    await bot.add_cog(MusicPlayerCog(bot))