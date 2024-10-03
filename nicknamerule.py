import random
from random import randint
import discord
from typing import Final

# changes a users nickname when either replying, directly pinging, or using a slash command with the phrase "they call you" [nickname]
# needs sanitisation, i.e a message "they call you in the morning" a users nickname shouldnt be changed to "in the morning"

#slash command, ping, and reply should all invoke the same code.

def nicknameprint(victim: discord.Member, newname: str): 
    newname = "**" + newname + "**"
    responses = [
    f"looks like {victim.mention} is going by {newname} now.. good for them!",
    f"hey {victim.mention}, heard they're calling you {newname}... your choice i suppose",
    f"{newname}.... really???",
    f"are you serious... {newname} is the best you could come up with..?",
    f"uh oh! the rule has been invoked {victim.mention}! you know what that means!!",
    f"{victim.mention} be like 'my name is {newname} dementia raven way'...",
    f"{victim.mention}, you know the rules...",
    f"i kinda feel sorry for {victim.mention} at this point.. or should i say {newname}...",
    f"{newname}, nice one +2",
    f"mfs be on some walter white shit like 'say my name' and their name is literally {newname}...",
    f"well well well... how the turn tables.. {victim.mention} is now {newname}",
    f"CONGRATULATIONS {victim.mention}! you have been selected to be the newest {newname}!",
    f"{victim.mention}... im sorry",
    f"they make me do this im sorry",
    f"r u kidding me...",
    f"IP. 92.28.211.234 N: 43.7462 W: 12.4893 \nSS Number: 6979191519182016\nIPv6: fe80::5dcd::ef69::fb22::d9888%12 \nUPNP:Enabled DMZ: 10.112.42.15 \nMAC:5A:78:3E:7E:00 \nISP: Ucom Universal DNS:8.8.8.8\n ALT DNS: 1.1.1.8.1 \nDNS SUFFIX:Dlink WAN: 100.23.10.15 \nGATEWAY:192.168.0.1 \nSUBNET MASK: 255.255.0.255\nUDP OPEN PORTS: 8080,80 \nTCP OPEN PORTS: 443\nROUTER VENDOR:ERICCSON \nDEVICE VENDOR: WIN32-X \nCONNECTION TYPE: Ethernet ICMP \nHOPS:192168.0.1 192168.1.1 100.73.43.4host-132.12.32.167.ucom.comhost-66.120.12.111.ucom.com36.134.67.189 216.239.78.111 sof02s32-in-f14.1e100.net \nTOTAL HOPS: 8 \nACTIVESERVICES: [HTTP]192.168.3.1:80=>92.28.211.234:80\n[HTTP]192.168.3.1:443=>92.28.211.234:443\n[UDP] 192.168.0.1:788=>192.168.1:6557\n[TCP]192.168.1.1:67891=>92.28.211.234:345\n[TCP]192.168.52.43:7777=>192.168.1.1:7778\n[TCP]192.168.78.12:898=>192.168.89.9:667\nEXTERNAL",
    f"HAHAHHAHAHAHAHAH {newname} LMAOOO!!! EVERYONE POINT AND LAUGH AT {victim.mention}",
    f"{victim.mention} is now {newname} na nite pal,,",
    f"{victim.mention} is now {newname}, as recompense they get 1 free pass to say whatever word they want!",
    f"hey kid, heard they callin' ya {newname} now...",
    f"they call you {newname}.",
    f"im so sick of this shit",
    f"wow yeah... they really DO call you {newname} thats so true",
    f"you dont have to tell me twice, but during the stone age...",
    f"wow! is that {victim.mention}? no... wait, its {newname}...",
    f"by the power invested in me i now pronounce you to be {newname}!",
    f"{victim.mention}, be glad its not..like.. idk, {victim.mention}smells.. or like {victim.mention}isgay or something",
    f"really not appropriate guys is it....",
    f"mfw they call you {newname}: <:beefstew:1285630081829437614>"
    ]
    
    response = random.choice(responses)
    return response

