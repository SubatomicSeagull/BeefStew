import discord
from discord.ext import commands
from beefcommands.utilities.music_player.queue import link_validation, queue_push, media_source, queue_list

class MusicPlayerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @discord.app_commands.command(name="play", description="add")
    async def play(self, interaction: discord.Interaction):
        await interaction.response.send_message("not implemented yet sorry :(")
        
    @discord.app_commands.command(name="play_next", description="play next, skip the queue!")
    async def play_next(self, interaction: discord.Interaction):
        await interaction.response.send_message("not implemented yet sorry :(")
        
    @commands.command(name="queue_add", description="add video to the queue")
    async def queue_add(self, ctx, url: str):
        media_type = await link_validation(url)
        print(f"Media type from link_validation: {media_type}")
        if media_type != "invalid" and media_type is not None:
            print(f"Valid {media_type} link...")
            yt_links = await media_source(ctx, url, media_type)
            print(f"yt_links returned from media_source: {yt_links}")
            print(f"Trying to push [YouTube Video](<{yt_links}>) to the queue")
            await queue_push(ctx, yt_links)
            await ctx.send(f"Pushed [YouTube Video](<{yt_links}>) to the queue successfully")
        else:
            await ctx.send("Invalid link")
        
    @commands.command(name="queue_list", description="list the queue")
    async def queue_list(self, ctx):
        await ctx.send(f"queue = {await queue_list(ctx)}")
        
    @discord.app_commands.command(name="skip", description="STREAMER NEXT GAME!!!!!!")
    async def skip(self, interaction: discord.Interaction):
        await interaction.response.send_message("not implemented yet sorry :(")
        
    @discord.app_commands.command(name="pause", description="STOP!!!!!")
    async def stop(self, interaction: discord.Interaction):
        await interaction.response.send_message("not implemented yet sorry :(")
        
    @discord.app_commands.command(name="loop", description="endless nameless...")
    async def loop(self, interaction: discord.Interaction):
        await interaction.response.send_message("not implemented yet sorry :(")
        
    @discord.app_commands.command(name="clear", description="clear the queue")
    async def clear(self, interaction: discord.Interaction):
        await interaction.response.send_message("not implemented yet sorry :(")
        
    @discord.app_commands.command(name="download", description="youtube yownloader")
    async def download(self, interaction: discord.Interaction):
        await interaction.response.send_message("not implemented yet sorry :(")

async def setup(bot):
    print("incantation cog setup")
    await bot.add_cog(MusicPlayerCog(bot))