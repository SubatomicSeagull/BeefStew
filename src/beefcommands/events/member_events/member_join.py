import discord
from beefutilities.guilds import read_guild_log_channel
from datetime import datetime

async def member_join_event(bot, member):
    # retrive the log channel
    channel_id = await read_guild_log_channel(member.guild.id)
    channel = await bot.fetch_channel(channel_id)
    await channel.send(embed=await join_message_embed(member, bot.user.avatar.url, member.guild.name))
    
async def join_message_embed(user: discord.Member, icon_url, guild_name):
        # embed header
        joinembed = discord.Embed(title=f"Hello!!!!!!!!", color=discord.Color.green())
        joinembed.set_thumbnail(url=user.avatar.url)
        # embed body
        joinembed.add_field(name="", value=f"<@{user.id}> **joined**", inline=False)
        joinembed.add_field(name="", value=f"Account created: `{user.created_at.strftime('%d/%m/%Y')}`", inline=False)
        joinembed.add_field(name="", value="", inline=False)
        joinembed.add_field(name="", value="", inline=False)
        joinembed.set_author(name="Beefstew", icon_url=icon_url)
        # embed footer
        joinembed.add_field(name="", value=f"{guild_name} - {datetime.now().strftime('%d/%m/%Y %H:%M')}")      
        return joinembed