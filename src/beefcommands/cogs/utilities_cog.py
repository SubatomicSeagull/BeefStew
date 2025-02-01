import discord
from discord.ext import commands
from beefcommands.utilities.ccping import ccping
from beefutilities.guilds import set_info, set_logs, set_quotes
from beefcommands.utilities.help import help

class UtilitiesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.app_commands.command(name="ccping", description="pings CCServer, please be responsible with this one...")
    async def ccping(self, interaction: discord.Interaction):
        await ccping(self.bot, interaction)
    
    @discord.app_commands.command(name="ccinfo", description="returns current info about CCServer")
    async def ccinfo(self, interaction: discord.Interaction, url: str):
        pass
    
    @discord.app_commands.command(name="set_logs_channel", description="where should i spew...?")
    async def set_log_channel(self, interacton: discord.Interaction):
        await set_logs(interacton)

    @discord.app_commands.command(name="set_info_channel", description="where should i spew...?")
    async def set_info_channel(self, interacton: discord.Interaction):
        await set_info(interacton)
    
    @discord.app_commands.command(name="set_quotes_channel", description="where do *you* spew...?")
    async def set_quote_channel(self, interacton: discord.Interaction):
        await set_quotes(interacton)
    
    @discord.app_commands.command(name="help", description="HELP!! HELP ME!!!!!!!")
    async def help(self, interaction: discord.Interaction):
        await help(self.bot, interaction)

async def setup(bot):
    print("utilities cog setup")
    await bot.add_cog(UtilitiesCog(bot))