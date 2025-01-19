import discord
from discord.ext import commands

class VisageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.group = discord.app_commands.Group(name="visage", description="alter the flesh, alter the mind...")
    
    async def cog_load(self):
        self.bot.tree.add_command(self.group)

    async def cog_unload(self):
        self.bot.tree.remove_command(self.group.name)