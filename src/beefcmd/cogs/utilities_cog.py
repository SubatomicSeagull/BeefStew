import discord
from discord.ext import commands

class UtilitiesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.group = discord.app_commands.Group(name="utilities", description="TOOLS!! i need my TOOLS!!!!!")
    
    async def cog_load(self):
        self.bot.tree.add_command(self.group)

    async def cog_unload(self):
        self.bot.tree.remove_command(self.group.name)