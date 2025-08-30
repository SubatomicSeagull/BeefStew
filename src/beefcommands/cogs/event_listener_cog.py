import discord
from discord.ext import commands
import beefcommands.events.message_events
from beefcommands.events.member_events.member_remove import member_remove_event
from beefcommands.events.member_events.member_join import member_join_event

class EventListenerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.kicked_members = set()
        self.banned_members = set()

    # message listener
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        await beefcommands.events.message_events.message_send_event(self.bot, message)

    # member join listener
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await member_join_event(self.bot, member)

    # member leave listener
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        await member_remove_event(self.bot, member, self.kicked_members, self.banned_members)

    # message edit listener
    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if not after.author.bot and before.content != after.content: print(f"> \033[32m{before.author.name} edited a message in #{before.channel.name}\033[0m")
        await beefcommands.events.message_events.message_edit_event(self.bot, before, after)

    # message delete listener
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if not message.author.bot and not "/say" in message.content.lower(): print(f"> \033[32m{message.author.name} deleted a message in #{message.channel.name}\033[0m")
        await beefcommands.events.message_events.message_delete_event(self.bot, message)

#    @commands.Cog.listener()
#    async def on_command(self, ctx):
#        print(f"> \033[34m{ctx.author.name} used /{ctx.command}\033[0m")

async def setup(bot):
    print("- \033[91mbeefcommands.cogs.event_listener_cog\033[0m")
    await bot.add_cog(EventListenerCog(bot))

