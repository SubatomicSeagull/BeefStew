import discord
from discord.ext import commands
import beefcommands.invocations.joker_score.change_joker_score
import beefcommands.invocations.joker_score.read_joker_score
import beefcommands.invocations.joker_score.gamble
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
        await beefcommands.invocations.joker_score.change_joker_score.plus2(interation, joker)
        
    # minus 2 manual command
    @discord.app_commands.command(name="minus2", description="*tugs on collar* yikes...")
    async def minus2(self, interation: discord.Interaction, joker: discord.Member):
        await beefcommands.invocations.joker_score.change_joker_score.minus2(interation, joker)
    
    # print the users score
    @discord.app_commands.command(name="score", description="how funny r u...?")
    async def score(self, interation: discord.Interaction, joker: discord.Member):
        await beefcommands.invocations.joker_score.read_joker_score.score(interation, joker)
      
    # gamble points  
    @discord.app_commands.command(name="gamble", description="Lets go gambling!")
    async def gamble(self, interation: discord.Interaction):
        await beefcommands.invocations.joker_score.gamble.gamble_points(interation)

async def setup(bot):
    print("invocation cog setup")
    await bot.add_cog(InvocationsCog(bot))