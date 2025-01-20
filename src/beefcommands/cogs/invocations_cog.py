import discord
from discord.ext import commands
import beefcommands.invocations.joker_score.change_joker_score
import beefcommands.invocations.joker_score.read_joker_score
from beefcommands.invocations.nickname_rule import invoke_nickname_rule

class InvocationsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="they_call_you", description="invokes the rule...")
    async def they_call_you(interaction: discord.Interaction, victim: discord.Member, new_name: str):
        await invoke_nickname_rule(interaction, victim, new_name)
        
    @discord.app_commands.command(name="plus2", description="good one buddy")
    async def plus2(interation: discord.Interaction, joker: discord.Member):
        await beefcommands.invocations.joker_score.change_joker_score.plus2(interation, joker)
        
    @discord.app_commands.command(name="minus2", description="*tugs on collar* yikes...")
    async def minus2(interation: discord.Interaction, joker: discord.Member):
        await beefcommands.invocations.joker_score.change_joker_score.minus2(interation, joker)
    
    @discord.app_commands.command(name="score", description="how funny r u...?")
    async def score(interation: discord.Interaction, joker: discord.Member):
        await beefcommands.invocations.joker_score.read_joker_score.score(interation, joker)

async def setup(bot):
    print("invocation cog setup")
    await bot.add_cog(InvocationsCog(bot))