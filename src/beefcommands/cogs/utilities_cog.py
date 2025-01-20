import discord
from discord.ext import commands
from beefcommands.utilities.ccping import ccping

class UtilitiesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.app_commands.command(name="ccping", description="pings CCServer, please be responsible with this one...")
    async def ccping(self, interaction: discord.Interaction):
        await ccping(self.bot, interaction)
    
    async def ccinfo():
        pass
    
    async def set_log_channel():
        pass

    async def set_info_channel():
        pass
    
    async def set_quote_channel():
        pass
    
    async def help():
        pass

async def setup(bot):
    print("utilities cog setup")
    await bot.add_cog(UtilitiesCog(bot))