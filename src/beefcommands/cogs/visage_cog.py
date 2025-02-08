import discord
from discord.ext import commands
import beefcommands.visage
import beefcommands.visage.JFK_pfp
import beefcommands.visage.add_speech_bubble_pfp
import beefcommands.visage.bless_pfp
import beefcommands.visage.boil_user_pfp
import beefcommands.visage.down_the_drain_pfp
import beefcommands.visage.gay_baby_jail_pfp

class VisageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # sends a picture of the users pfp boiled
    @discord.app_commands.command(name="boil", description="focken boil yehs")
    async def boil(self, interaction: discord.Interaction, victim: discord.Member):
        await beefcommands.visage.boil_user_pfp.boil(interaction, victim)
    
    # sends a picture of the users pfp with a speech bubble
    @discord.app_commands.command(name="slander", description="i cant belive they said that")
    async def slander(self, interaction: discord.Interaction, victim: discord.Member):
        await beefcommands.visage.add_speech_bubble_pfp.slander(interaction, victim)
    
    # sends a picture of the users pfp down a drain
    @discord.app_commands.command(name="down_the_drain", description="yeah sorry we dropped them in there we cant get them out ://")
    async def down_the_drain(self, interaction: discord.Interaction, victim: discord.Member):
        await beefcommands.visage.down_the_drain_pfp.down_the_drain(interaction, victim)
    
    # sends a picture of the user in jail
    @discord.app_commands.command(name="jail", description="gay baby jail")
    async def jail(self, interaction: discord.Interaction, victim: discord.Member):
        await beefcommands.visage.gay_baby_jail_pfp.GBJ(interaction, victim)

    # sends a picture of the user being held by jesus
    @discord.app_commands.command(name="bless", description="bless you my child")
    async def bless(self, interaction: discord.Interaction, victim: discord.Member):
        await beefcommands.visage.bless_pfp.bless(interaction, victim)
    
    # sends a picture of the users pfp in the jfk car lol
    @discord.app_commands.command(name="jfk", description="MR PRESIDENT GET DOWN!!!!")
    async def JFK(self, interaction: discord.Interaction, victim: discord.Member):
        await beefcommands.visage.JFK_pfp.watch_out(interaction, victim)

async def setup(bot):
    print("visage cog setup")
    await bot.add_cog(VisageCog(bot))