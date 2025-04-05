import discord
from discord.ext import commands
from beefcommands.visage import react, down_the_drain_pfp, boil_user_pfp, add_speech_bubble_pfp, bless_pfp, JFK_pfp, gay_baby_jail_pfp



class VisageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # sends a picture of the users pfp boiled
    @discord.app_commands.command(name="boil", description="focken boil yehs")
    async def boil(self, interaction: discord.Interaction, victim: discord.Member):
        print(f"> \033[32m{interaction.user.name} used /boil on {victim.name}\033[0m")
        await boil_user_pfp.boil(interaction, victim)
    
    # sends a picture of the users pfp with a speech bubble
    @discord.app_commands.command(name="slander", description="i cant belive they said that")
    async def slander(self, interaction: discord.Interaction, victim: discord.Member):
        print(f"> \033[32m{interaction.user.name} used /slander on {victim.name}\033[0m")
        await add_speech_bubble_pfp.slander(interaction, victim)
    
    # sends a picture of the users pfp down a drain
    @discord.app_commands.command(name="down_the_drain", description="yeah sorry we dropped them in there we cant get them out ://")
    async def down_the_drain(self, interaction: discord.Interaction, victim: discord.Member):
        print(f"> \033[32m{interaction.user.name} used /down_the_drain on {victim.name}\033[0m")
        await down_the_drain_pfp.down_the_drain(interaction, victim)
    
    # sends a picture of the user in jail
    @discord.app_commands.command(name="jail", description="gay baby jail")
    async def jail(self, interaction: discord.Interaction, victim: discord.Member):
        print(f"> \033[32m{interaction.user.name} used /jail on {victim.name}\033[0m")
        await gay_baby_jail_pfp.GBJ(interaction, victim)

    # sends a picture of the user being held by jesus
    @discord.app_commands.command(name="bless", description="bless you my child")
    async def bless(self, interaction: discord.Interaction, victim: discord.Member):
        print(f"> \033[32m{interaction.user.name} used /bless on {victim.name}\033[0m")
        await bless_pfp.bless(interaction, victim)
    
    # sends a picture of the users pfp in the jfk car lol
    @discord.app_commands.command(name="jfk", description="MR PRESIDENT GET DOWN!!!!")
    async def JFK(self, interaction: discord.Interaction, victim: discord.Member):
        print(f"> \033[32m{interaction.user.name} used /jfk on {victim.name}\033[0m")
        await JFK_pfp.watch_out(interaction, victim)
        


# cog startup
async def setup(bot):
    print("- \033[96mbeefcommands.cogs.visage_cog\033[0m")
    await bot.add_cog(VisageCog(bot))
    
    # load the context menu commands
    from beefcommands.cogs.visage_context_menu import setup as visage_context_menu_setup
    await visage_context_menu_setup(bot)
    
