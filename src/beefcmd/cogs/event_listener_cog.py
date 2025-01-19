import discord
from discord.ext import commands
import beefcmd.events.message_events
from beefcmd.events.member_events.member_remove import member_remove_event
from beefcmd.events.member_events.member_join import member_join_event

class EventListenerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.kicked_members = set()
        self.banned_members = set()

    # Message Listener
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        await beefcmd.events.message_events.message_send_event(self.bot, message)

    # Member Join Listener
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await member_join_event(self.bot, member)

    # Member Leave Listener
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        await member_remove_event(self.bot, member, self.kicked_members, self.banned_members)

    # Message Edit Listener
    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        await beefcmd.events.message_events.message_edit_event(self.bot, before, after)

    # Message Delete Listener
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        beefcmd.events.message_events.message_delete_event(self.bot, message)

async def setup(bot):
    print("event cog setup")
    await bot.add_cog(EventListenerCog(bot))
