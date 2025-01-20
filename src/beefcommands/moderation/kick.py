import discord
from json_handling import load_element
from datetime import datetime
import random
import os
from guilds import read_guild_log_channel
from data import postgres

async def kick_member(interaction: discord.Interaction, bot, member: discord.Member, reason: str, kicked_members: set): 
    if interaction.user.id == member.id:
        await interaction.response.send_message("u cant kick youself idiot, the leave button is right there", ephemeral=True)
        return
    if member.id == os.getenv("CLIENTID"):
        await interaction.response.send_message("you cant get rid of me that easily...", ephemeral=True)
        return
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("yeah yeah nice try", ephemeral=True)
        return
    
    try:    
        kicked_members.add(member.id)
        channelid = await read_guild_log_channel(interaction.guild.id)
        channel = await bot.fetch_channel(channelid)
        await channel.send(embed=await kick_message_embed(interaction.user, member, reason, bot.user.avatar.url, interaction.guild.name))
        await interaction.response.send_message(f"You kicked {member.name}.", ephemeral=True)
        await member.kick(reason=reason)
    except Exception as e:
        print(e)
        await postgres.log_error(e)
        await interaction.response.send_message(f"Couldn't kick user {member.name} because {e}", ephemeral=True)

async def kick_message_embed(mod: discord.Member, member: discord.Member, reason: str, icon_url, guild_name):
        kickembed = discord.Embed(title=f"Kicked!", color=discord.Color.dark_orange())
        kickembed.set_thumbnail(url=member.avatar.url)
        kickembed.add_field(name="", value=get_kick_message(member, reason), inline=False)
        kickembed.add_field(name="", value="", inline=False)
        kickembed.add_field(name="", value="", inline=False)
        kickembed.add_field(name="", value="", inline=False)
        kickembed.add_field(name="", value=f"**Kicked by**: <@{mod.id}>", inline=False)
        kickembed.add_field(name="", value=f"**Reason**: {reason}", inline=False)    
        kickembed.add_field(name="", value="", inline=False)
        kickembed.add_field(name="", value="", inline=False) 
        kickembed.set_author(name="Beefstew", icon_url=icon_url)
        kickembed.add_field(name="", value=f"{guild_name} - {datetime.now().strftime('%d/%m/%Y %H:%M')}")      
        return kickembed

def get_kick_message(member: discord.Member, reason: str): 
    membername = type('Member', (object,), {"id": member.id})()
    responses = load_element("responses.json", "kick_messages")    
    chosen_response = random.choice(responses).format(member=membername, reason=reason)
    return chosen_response