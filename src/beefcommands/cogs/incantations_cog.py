import discord
from discord.ext import commands
import beefcommands.incantations.vicious_mockery
import beefcommands.incantations.poke

class IncantationsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # vicious mockery
    @discord.app_commands.command(name="mock", description="cast vicious mockery on someone")
    async def vicious_mockery(self, interaction: discord.Interaction, victim: discord.Member):
        print(f"> \033[32m{interaction.user.name} mocked {victim.name}\033[0m")
        await beefcommands.incantations.vicious_mockery.insult(interaction, victim)

    # poke
    @discord.app_commands.command(name="poke", description="poke someone")
    async def poke(self, interaction: discord.Interaction, victim: discord.Member, dm: bool, private: bool):
        print(f"> \033[32m{interaction.user.name} poked {victim.name}\033[0m")
        await beefcommands.incantations.poke.pokeuser(interaction, victim, dm, private, self.bot)

# cog startup
async def setup(bot):
    print("- \033[93mbeefcommands.cogs.incantations_cog\033[0m")
    await bot.add_cog(IncantationsCog(bot))