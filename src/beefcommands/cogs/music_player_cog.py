import asyncio
from discord.ext import commands
from beefutilities import voice_channel
from beefcommands.utilities.music_player import player
from beefcommands.utilities.music_player import queue


class MusicPlayerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.disconnect_task = None
        
    def cancel_disconnect_time(self):
        if self.disconnect_task and not self.disconnect_task.done():
            self.disconnect_task.cancel()
            self.disconnect_task = None    
    
    @commands.command(name="join", description="get in here!!")
    async def cog_join_vc(self, ctx):
        await voice_channel.join_vc(ctx)
    
    @commands.command(name="leave", aliases=["fuckoff"],  description="fukoff")
    async def cog_leave_vc(self, ctx):
        await voice_channel.leave_vc(ctx)

    @commands.command(name="play", aliases=["p"], description="play the funky music white boy")
    async def cog_play(self, ctx, *args):
        player.play(ctx, *args)

    @commands.command(name="pause", description="Pauses the current track")
    async def cog_pause(self, ctx):
        player.pause(ctx)

    @commands.command(name="resume", description="Resumes the paused track")
    async def cog_resume(self, ctx):
        player.resume(ctx)
    
    @commands.command(name="skip", aliases=["next"], description="next pleaes")
    async def cog_skip(self, ctx):
        player.skip
    
    @commands.command(name="queue", aliases=["q"], description="add something to the back of the queue")
    async def cog_queue(self, ctx, *args):
        await queue.qadd(ctx, *args)
    
    @commands.command(name="queuelist", aliases=["qlist", "list", "queue_list", "listqueue", "list_queue"], description="lists the queue")
    async def cog_queue_list(self, ctx):
        await queue.qlist(ctx)
         
    @commands.command(name="queueclear", aliases=["qclear", "clear", "queue_clear", "clear_queue"])
    async def cog_queue_clear(self, ctx):
        await queue.qclear(ctx)
        
    @commands.command(name="shuffle", description="shuffle the queue")
    async def cog_queue_shuffle(self, ctx):
        await queue.qshuffle(ctx)
    
    @commands.command(name="loop", aliases=["repeat"], description="loop the current song")
    async def cog_loop_queue(self, ctx):
        await queue.qloop(ctx)
        
async def setup(bot):
    print("incantation cog setup")
    await bot.add_cog(MusicPlayerCog(bot))