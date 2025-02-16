import discord
from discord.ext import commands
import beefcommands.moderation.mute
import beefcommands.moderation.kick
import beefcommands.moderation.ban

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.kicked_members = set()
        self.banned_members = set()
    
    # /kick
    @discord.app_commands.command(name="kick", description="foekn get 'em yea")
    async def kick(self, interaction: discord.Interaction, user: discord.Member, reason: str):
        print(f"> \033[32m{interaction.user.name} used /kick on {user.name}\033[0m")
        await beefcommands.moderation.kick.kick_member(interaction, self.bot, user, reason, self.kicked_members)
    
    # /ban
    @discord.app_commands.command(name="ban", description="KILL! KILL! KILL! KILL!!!!!")
    async def ban(self, interaction: discord.Interaction, user: discord.Member, reason: str):
        print(f"> \033[32m{interaction.user.name} used /ban on {user.name}\033[0m")
        await beefcommands.moderation.ban.ban_member(interaction, self.bot, user, reason, self.banned_members)
    
    # /mute
    @discord.app_commands.command(name="mute", description="SHHHHH")
    async def mute(self, interaction: discord.Interaction, member: discord.Member):
        print(f"> \033[32m{interaction.user.name} used /mute on {member.name}\033[0m")
        await beefcommands.moderation.mute.mute(interaction, member)
    
    # /unmute
    @discord.app_commands.command(name="unmute", description="you may speak...")
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        print(f"> \033[32m{interaction.user.name} used /unmute on {member.name}\033[0m")
        await beefcommands.moderation.mute.unmute(interaction, member)

# cog startup
async def setup(bot):
    print("- \033[92mbeefcommands.cogs.moderation_cog\033[0m")
    await bot.add_cog(ModerationCog(bot))