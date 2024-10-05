import discord
from discord.ext import commands
import random

# TBD 
#   >   need some way to pass in the log channel id
#   >   implement more ban messages
#   >   warn system for spam, x warns and a user is kicked for exceeding the warning threshold
#   >   also option to manually warn or clear warnings from people
#   >   ability to mute / assign and remove muted role 

def get_kick_message(member: discord.Member, reason: str):
    kick_messages = [
        f"{member.name} was kicked. see ya, asshole",
        f"{member.name} was kicked for {reason}, sounds about right",
        f"looks like {member.name} wont be joining us for dinner... they {reason} and got kicked",
        f"lmao bye {member.name}",
        f"{reason}... yeah... that'll do it",
        f"{member.name} sayonara you weeabo shit",
        f"{member.name} fuck off",
        f"{member.name} was kicked, but remember, a kick is only temporary, but a ban.. thats for life babey!"
        f"its sooo like {member.name} to be kicked for {reason}"
        ]
    return random.choice(kick_messages)

def get_ban_message(member: discord.Member, reason: str):
    ban_messages = [
        f"{member.name} was banned. see ya, asshole",
        f"{member.name} was kicked for {reason}, sounds about right",
        f"{member.name} was banned! they wont be {reason} again",
        f"",
        f"",
        f"",
        f"",
    ]
    return random.choice(ban_messages)

async def kick_member(interaction: discord.Interaction, member: discord.Member, reason: str):
    if reason == "": reason += "uhh, doing whatever it is they were doing"
    await member.kick(reason=reason)
    #await bot.get_channel(logs_channel).send(random.choice(get_kick_message(member, reason)))
    return

async def ban_member(interaction: discord.Interaction, member: discord.Member, reason: str):
    if reason == "": reason += "uhh, doing whatever it is they were doing"
    await member.ban(reason=reason)
    #await bot.get_channel(logs_channel).send(random.choice(get_ban_message(member, reason)))
    return

