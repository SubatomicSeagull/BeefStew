import discord
from discord.ext import commands
import beefcmd.incantations.vicious_mockery

class IncantationsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @discord.app_commands.command(name="vicious_mockery", description="cast vicious mockery on someone")
    async def vicious_mockery(self, interaction: discord.Interaction, victim: discord.Member):
        await beefcmd.incantations.vicious_mockery.insult(interaction, victim)

async def setup(bot):
    print("incantation cog setup")
    await bot.add_cog(IncantationsCog(bot))