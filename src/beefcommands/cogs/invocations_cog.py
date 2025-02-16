import discord
from discord.ext import commands
from beefcommands.invocations.joker_score import change_joker_score, read_joker_score, gamble, leaderboard
from beefcommands.invocations.nickname_rule import invoke_nickname_rule

class InvocationsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # they call u manual command
    @discord.app_commands.command(name="they_call_you", description="invokes the rule...")
    async def they_call_you(self, interaction: discord.Interaction, victim: discord.Member, new_name: str):
        await invoke_nickname_rule(interaction, victim, new_name)
        
    # plus 2 manual command
    @discord.app_commands.command(name="plus2", description="good one buddy")
    async def plus2(self, interation: discord.Interaction, joker: discord.Member):
        await change_joker_score.plus2(interation, joker)
        
    # minus 2 manual command
    @discord.app_commands.command(name="minus2", description="*tugs on collar* yikes...")
    async def minus2(self, interation: discord.Interaction, joker: discord.Member):
        await change_joker_score.minus2(interation, joker)
    
    # print the users score
    @discord.app_commands.command(name="score", description="how funny r u...?")
    async def score(self, interaction: discord.Interaction, joker: discord.Member):
        print(f"> \033[32m{interaction.user.name} used /score on {joker.name}\033[0m")
        await read_joker_score.score(interaction, joker)
      
    @discord.app_commands.command(name="leaderboard", description="whos the funniest huh??")
    async def leaderboard(self, interaction: discord.Interaction):
        print(f"> \033[32m{interaction.user.name} used /leaderboard\033[0m")
        await leaderboard.retrive_top_scores(interaction, self.bot)
      
    @discord.app_commands.command(name="loserboard", description="whos not the funniest huh??")
    async def loserboard(self, interaction: discord.Interaction):
        print(f"> \033[32m{interaction.user.name} used /loserboard\033[0m")
        await leaderboard.retrive_low_scores(interaction, self.bot)  
      
      
    # gamble points  
    @discord.app_commands.command(name="gamble", description="Lets go gambling!")  
    async def gamble(self, interaction: discord.Interaction):
        print(f"> \033[32m{interaction.user.name} used /gamble\033[0m")
        await gamble.gamble_points(interaction)

# cog startup
async def setup(bot):
    print("- \033[33mbeefcommands.cogs.invocations_cog\033[0m")
    await bot.add_cog(InvocationsCog(bot))