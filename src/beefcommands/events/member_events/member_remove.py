import discord
from beefutilities.guilds.text_channel import read_guild_log_channel
from datetime import datetime


async def member_remove_event(bot, member: discord.Member, kicked_members, banned_members):
        #  check the kicked and banned members holding list, dont send leave message
        if member.id in kicked_members:
            kicked_members.remove(member.id)
            return
        if member.id in banned_members:
            banned_members.remove(member.id)
            return
        # retreive the log channel
        channel_id = await read_guild_log_channel(member.guild.id)
        channel = await bot.fetch_channel(channel_id)
        await channel.send(embed=await leave_message_embed(member, bot, member.guild.name))
        
async def leave_message_embed(user: discord.Member, bot, guild_name):
    user = await bot.fetch_user(user.id)
    
    # embed header
    leaveembed = discord.Embed(title=f"cya", color=discord.Color.purple())
    leaveembed.set_thumbnail(url=user.avatar.url)
    # embed body
    leaveembed.add_field(name="", value=f"@{user.name} **left.**", inline=False)
    leaveembed.add_field(name="", value="", inline=False)
    leaveembed.add_field(name="", value="", inline=False)
    leaveembed.set_author(name="Beefstew", icon_url=bot.user.avatar.url)
    # embed footer
    leaveembed.add_field(name="", value=f"{guild_name} - {datetime.now().strftime('%d/%m/%Y - %H:%M')}")      
    return leaveembed