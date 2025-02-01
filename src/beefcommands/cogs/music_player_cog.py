import discord
from discord.ext import commands
import yt_dlp
import requests
import re
from beefcommands.utilities.music_player.queue import link_validation, queue_push, media_source, queue_list
import asyncio

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
        await asyncio.to_thread(await self.queue_add_sync, ctx, url)
            
    async def queue_add_sync(ctx, link,):
        media_type = await link_validation(url)
        print(f"Media type from link_validation: {media_type}")
        if media_type != "invalid" and media_type is not None:
            print(f"Valid {media_type} link...")
            yt_links = await media_source(ctx, url, media_type)
            count = 0
            for playlist in yt_links:
                for link in playlist:
                    print (f"Link: {link}")
                    
                    response  = requests.get(link)
                    title_match = re.search(r'<title>(.*?) - YouTube</title>', response.text)
                    if title_match:
                        title = title_match.group(1).strip()
                        
                    print(f"Adding [{title}]({link}) to the queue")
                    asyncio.to_thread(queue_push(ctx, link))
                    count+=1

            await ctx.send(f"Pushed **{count}** track(s) to the queue successfully")
        else:
            await ctx.send("Invalid link")
        
            
            

        
    @commands.command(name="queue_list", description="list the queue")
    async def queue_list(self, ctx):
        await ctx.send(await asyncio.to_thread(queue_list, ctx))
        
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