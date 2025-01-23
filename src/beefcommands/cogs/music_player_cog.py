import discord
from discord.ext import commands

class MusicPlayerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @discord.app_commands.command(name="play", description="add")
    async def play(self, interaction: discord.Interaction):
        await interaction.response.send_message("not implemented yet sorry :(")
        
    @discord.app_commands.command(name="play_next", description="play next, skip the queue!")
    async def play_next(self, interaction: discord.Interaction):
        await interaction.response.send_message("not implemented yet sorry :(")
        
    @discord.app_commands.command(name="queue", description="add video to the queue")
    async def queue(self, interaction: discord.Interaction):
        await interaction.response.send_message("not implemented yet sorry :(")
        
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