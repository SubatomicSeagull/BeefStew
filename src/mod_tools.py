import discord
from discord.ext import commands
import random
import json
import os
from datetime import datetime

# TBD 
#   >   implement more ban messages
#   >   warn system for spam, x warns and a user is kicked for exceeding the warning threshold
#   >   also option to manually warn or clear warnings from people
#   >   ability to mute / assign and remove muted role 
    
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
    responses = load_responses("src\\assets\\responses.json", "kick_messages")    
    chosen_response = random.choice(responses).format(member=membername, reason=reason)
    return chosen_response

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
    responses = load_responses("src\\assets\\responses.json", "ban_messages")    
    chosen_response = random.choice(responses).format(member=membername, reason=reason)
    return chosen_response

async def join_message_embed(user: discord.Member, icon_url, guild_name):
        joinembed = discord.Embed(title=f"Hello!!!!!!!!", color=discord.Color.green())
        joinembed.set_thumbnail(url=user.avatar.url)
        joinembed.add_field(name="", value=f"<@{user.id}> **joined**", inline=False)
        joinembed.add_field(name="", value=f"Account created: `{user.created_at.strftime('%d/%m/%Y')}`", inline=False)
        joinembed.add_field(name="", value="", inline=False)
        joinembed.add_field(name="", value="", inline=False)
        joinembed.set_author(name="Beefstew", icon_url=icon_url)
        joinembed.add_field(name="", value=f"{guild_name} - {datetime.now().strftime('%d/%m/%Y %H:%M')}")      
        return joinembed
    
async def leave_message_embed(user: discord.Member, icon_url, guild_name):
        leaveembed = discord.Embed(title=f"cya", color=discord.Color.purple())
        leaveembed.set_thumbnail(url=user.avatar.url)
        leaveembed.add_field(name="", value=f"<@{user.id}> **left.**", inline=False)
        leaveembed.add_field(name="", value="", inline=False)
        leaveembed.add_field(name="", value="", inline=False)
        leaveembed.set_author(name="Beefstew", icon_url=icon_url)
        leaveembed.add_field(name="", value=f"{guild_name} - {datetime.now().strftime('%d/%m/%Y %H:%M')}")      
        return leaveembed

def load_responses(file_path, element):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data[element]

def read_log_channel(guild_id):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'assets', 'guild_config.json')

    with open(file_path, "r") as file:
        data = json.load(file)
        
    if guild_id == data["guild"]["id"]:
         return data["guild"]["channel_id"]
    else:
        return "" 
        
def read_guild_id():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'assets', 'guild_config.json')

    with open(file_path, "r") as file:
        data = json.load(file)
    return data["guild"]["id"]

async def write_guild_id(guild_id, channel_id):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'assets', 'guild_config.json')
    
    data = {"guild": {}}
    data["guild"]["id"] = str(guild_id)
    print(f"wrote {guild_id} in guild:id")
    data["guild"]["channel_id"] = str(channel_id)
    print(f"wrote {channel_id} in guild:channel_id")
    
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
