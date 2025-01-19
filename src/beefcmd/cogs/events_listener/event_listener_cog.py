import os
from dotenv import load_dotenv
import discord
from discord import Message
from discord.ext import commands
from nickname_rule import *
from mod_tools import *
from responses import *
from data.server_info.ping import pingembed
from pfp_manipulations import *
from help import *
from json_handling import *
from joker_score import *
from guilds import *
from random import randint
from time import sleep
from beefcmd.cogs.events_listener.member_events.member_remove import member_remove_event
from beefcmd.cogs.events_listener.member_events.member_join import member_join_event
import beefcmd.cogs.events_listener.message_events

class EventListenerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.kicked_members = set()
        self.banned_members = set()

    # Message Listener
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        await beefcmd.cogs.events_listener.message_events.message_send_event(self.bot, message)

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
        await beefcmd.cogs.events_listener.message_events.message_edit_event(self.bot, before, after)

    # Message Delete Listener
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        beefcmd.cogs.events_listener.message_events.message_delete_event(self.bot, message)

async def setup(bot):
    await bot.add_cog(EventListenerCog(bot))
