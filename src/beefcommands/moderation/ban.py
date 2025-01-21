import discord
from beefutilities.json_handling import load_element
from datetime import datetime
import random
import os
from beefutilities.guilds import read_guild_log_channel
from data import postgres

async def ban_member(interaction: discord.Interaction, bot, member: discord.Member, reason: str, banned_members: set): 
    if interaction.user.id == member.id:
        await interaction.response.send_message("You can't ban youself idiot, the leave button is right there", ephemeral=True)
        return
    if member.id == os.getenv("CLIENTID"):
        await interaction.response.send_message("you cant get rid of me that easily...", ephemeral=True)
        return
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("you really think im gonna let u do that?", ephemeral=True)
        return
    
    try:
        banned_members.add(member.id)    
        channelid = await read_guild_log_channel(interaction.guild.id)
        channel = await bot.fetch_channel(channelid)
        await channel.send(embed=await ban_message_embed(interaction.user, member, reason, bot.user.avatar.url, interaction.guild.name))
        await interaction.response.send_message(f"You banned {member.name}.", ephemeral=True)
        await member.ban(reason=reason)
    except Exception as e:
        await postgres.log_error(e)
        await interaction.response.send_message(f"Couldn't ban user {member.name} because {e}", ephemeral=True)

async def ban_message_embed(mod: discord.Member, member: discord.Member, reason: str, icon_url, guild_name):
        banembed = discord.Embed(title=f"BANNED!", color=discord.Color.red())
        banembed.set_thumbnail(url=member.avatar.url)
        banembed.add_field(name="", value=get_ban_message(member, reason), inline=False)
        banembed.add_field(name="", value="", inline=False)
        banembed.add_field(name="", value="", inline=False)
        banembed.add_field(name="", value="", inline=False)
        banembed.add_field(name="", value=f"**Banned by**: <@{mod.id}>", inline=False)
        banembed.add_field(name="", value=f"**Reason**: {reason}", inline=False)    
        banembed.add_field(name="", value="", inline=False)
        banembed.add_field(name="", value="", inline=False) 
        banembed.set_author(name="Beefstew", icon_url=icon_url)
        banembed.add_field(name="", value=f"{guild_name} - {datetime.now().strftime('%d/%m/%Y %H:%M')}")      
        return banembed
    
def get_ban_message(member: discord.Member, reason: str): 
    membername = type('Member', (object,), {"id": member.name})()
    responses = load_element("responses.json", "ban_messages")    
    chosen_response = random.choice(responses).format(member=membername, reason=reason)
    return chosen_response