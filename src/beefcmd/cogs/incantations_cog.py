import discord
from discord.ext import commands

class IncantationsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @discord.app_commands.command(name="vicious_mockery", description="cast vicious mockery on someone")
    async def vicious_mockery(self, interaction: discord.Interaction, victim: discord.Member):
        print("fuck")

async def setup(bot):
    print("incantation cog setup")
    await bot.add_cog(IncantationsCog(bot))