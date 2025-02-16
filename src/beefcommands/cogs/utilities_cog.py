import discord
from discord.ext import commands
from beefcommands.utilities.ccping import ccping
from beefutilities.guilds import set_info, set_logs, set_quotes
from beefcommands.utilities.help import help
from beefutilities.update import update_info

class UtilitiesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # pings ccserver and returns an average ping time
    @discord.app_commands.command(name="ccping", description="pings CCServer, please be responsible with this one...")
    async def ccping(self, interaction: discord.Interaction):
        print(f"> \033[32m{interaction.user.name} used /ccping\033[0m")
        await ccping(self.bot, interaction)
    
    # not implemented yet, will retrive info about ccserver like storage, ping, etc
    @discord.app_commands.command(name="ccinfo", description="returns current info about CCServer")
    async def ccinfo(self, interaction: discord.Interaction, url: str):
        pass
    
    # sets the logs channel to the channel its run in
    @discord.app_commands.command(name="set_logs_channel", description="where should i spew...?")
    async def set_log_channel(self, interaction: discord.Interaction):
        print(f"> \033[32m{interaction.user.name} used /set_log_channel in #{interaction.channel.name}\033[0m")
        await set_logs(interaction)

    # sets the info channel to the channel its run in
    @discord.app_commands.command(name="set_info_channel", description="where should i spew...?")
    async def set_info_channel(self, interaction: discord.Interaction):
        print(f"> \033[32m{interaction.user.name} used /set_info_channel in #{interaction.channel.name}\033[0m")
        await set_info(interaction)
    
    # sets the quotes channel to the channel its run in
    @discord.app_commands.command(name="set_quotes_channel", description="where do *you* spew...?")
    async def set_quote_channel(self, interaction: discord.Interaction):
        print(f"> \033[32m{interaction.user.name} used /set_quotes_channel in #{interaction.channel.name}\033[0m")
        await set_quotes(interaction)
    
    # prints a list of commands
    @discord.app_commands.command(name="help", description="HELP!! HELP ME!!!!!!!")
    async def help(self, interaction: discord.Interaction):
        print(f"> \033[32m{interaction.user.name} used /help\033[0m")
        await help(self.bot, interaction)
        
    #prints the patchnotes in a nice litte embed
    @discord.app_commands.command(name="update", description="whats new?")
    async def update(self, interaction: discord.Interaction):
        print(f"> \033[32m{interaction.user.name} used update\033[0m")
        await update_info(interaction, self.bot)    
    
    @discord.app_commands.command(name="test", description="jamie delete this")
    async def test(self, interaction: discord.Interaction):
        await update_info(interaction, self.bot)

# cog setup
async def setup(bot):
    print("- \033[32mbeefcommands.cogs.utilities_cog\033[0m")
    await bot.add_cog(UtilitiesCog(bot))