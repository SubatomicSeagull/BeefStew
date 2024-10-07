import discord
from discord.ext import commands
import random
import json

# TBD 
#   >   need some way to pass in the log channel id
#   >   implement more ban messages
#   >   warn system for spam, x warns and a user is kicked for exceeding the warning threshold
#   >   also option to manually warn or clear warnings from people
#   >   ability to mute / assign and remove muted role 

async def kick_member(interaction: discord.Interaction, member: discord.Member, reason: str):
    await member.kick(reason=reason)
    # wont work as theres no way of storing the log channel ID yet
    # await bot.get_channel(logs_channel).send(get_kick_message(member, reason))
    return

async def ban_member(interaction: discord.Interaction, member: discord.Member, reason: str):
    await member.ban(reason=reason)
    # wont work as theres no way of storing the log channel ID yet
    # await bot.get_channel(logs_channel).send(get_ban_message(member, reason))
    return

def get_kick_message(member: discord.Member, reason: str): 
    membername = type('Member', (object,), {"name": member.name})()
    responses = load_responses("src\\assets\\responses.json", "kick_messages")    
    chosen_response = random.choice(responses).format(member=membername, reason=reason)
    return chosen_response

def get_ban_message(member: discord.Member, reason: str): 
    membername = type('Member', (object,), {"name": member.name})()
    responses = load_responses("src\\assets\\responses.json", "ban_messages")    
    chosen_response = random.choice(responses).format(member=membername, reason=reason)
    return chosen_response

def load_responses(file_path, element):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data[element]