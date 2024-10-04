import random
import discord

# changes a users nickname when either replying, directly pinging, or using a slash command with the phrase "they call you" [nickname]
# needs sanitisation, i.e a message "they call you in the morning" a users nickname shouldnt be changed to "in the morning"

#slash command, ping, and reply should all invoke the same code.

#nickname rule, handles logic for they call you slash command
async def change_nickname(intormessage, victim: discord.Member, new_name: str):
    #checks to see if the interaction is through an interaction object or a message object, effectivly switches between using the slash command and having the command run inline
        if isinstance(intormessage, discord.Interaction):
            interaction = intormessage
            # not allowed to rename the bot
            if victim.id != 1283805971524747304:
                # not allowed to rename yourself
                if victim.id == interaction.user.id:
                    await interaction.response.send_message(f"**{interaction.user.name}** tried to invoke the rule on themselves... for some reason")
                else:
                    try:
                        await victim.edit(nick=new_name)
                        await interaction.response.send_message(f"**{interaction.user.name}** invoked the rule on **{victim.name}**!\n{nicknameprint(victim, new_name)}")           
                    except discord.Forbidden as e:
                        print(e)
                        await interaction.response.send_message(f"**{interaction.user.name}** tried to invoked the rule on **{victim.name}**!\nbut it didnt work :( next time get some permissions okay?")
                    except Exception as e:
                        print(e)
            else:
                await interaction.response.send_message(f"**{interaction.user.name}** tried to invoked the rule on **{victim.name}**!\nnice try fucker...")
                
        elif isinstance(intormessage, discord.Message):
            message = intormessage
            # not allowed to rename the bot
            if victim.id != 1283805971524747304:
                # not allowed to rename yourself
                if victim.id == message.author.id:
                    await message.channel.send(f"**{message.author.name}** tried to invoke the rule on themselves... for some reason")
                else:
                    try:
                        await victim.edit(nick=new_name)
                        await message.channel.send(f"**{message.author.name}** invoked the rule on **{victim.name}**!\n{nicknameprint(victim, new_name)}")
                    except Exception as e:
                        print(e)
                        await message.channel.send(f"**{message.author.name}** tried to invoked the rule on **{victim.name}**!\nbut it didnt work :( next time get some permissions okay?")
            else:
                await message.channel.send(f"**{message.author.name}** tried to invoked the rule on **{victim.name}**!\nnice try fucker...")



def nicknameprint(victim: discord.Member, new_name: str): 
    new_name = "**" + new_name + "**"
    responses = [
    f"looks like {victim.mention} is going by {new_name} now.. good for them!",
    f"hey {victim.mention}, heard they're calling you {new_name}... your choice i suppose",
    f"{new_name}.... really???",
    f"are you serious... {new_name} is the best you could come up with..?",
    f"uh oh! the rule has been invoked {victim.mention}! you know what that means!!",
    f"{victim.mention} be like 'my name is {new_name} dementia raven way'...",
    f"{victim.mention}, you know the rules...",
    f"i kinda feel sorry for {victim.mention} at this point.. or should i say {new_name}...",
    f"{new_name}, nice one +2",
    f"mfs be on some walter white shit like 'say my name' and their name is literally {new_name}...",
    f"well well well... how the turn tables.. {victim.mention} is now {new_name}",
    f"CONGRATULATIONS {victim.mention}! you have been selected to be the newest {new_name}!",
    f"{victim.mention}... im sorry",
    f"they make me do this im sorry",
    f"r u kidding me...",
    f"IP. 92.28.211.234 N: 43.7462 W: 12.4893 \nSS Number: 6979191519182016\nIPv6: fe80::5dcd::ef69::fb22::d9888%12 \nUPNP:Enabled DMZ: 10.112.42.15 \nMAC:5A:78:3E:7E:00 \nISP: Ucom Universal DNS:8.8.8.8\n ALT DNS: 1.1.1.8.1 \nDNS SUFFIX:Dlink WAN: 100.23.10.15 \nGATEWAY:192.168.0.1 \nSUBNET MASK: 255.255.0.255\nUDP OPEN PORTS: 8080,80 \nTCP OPEN PORTS: 443\nROUTER VENDOR:ERICCSON \nDEVICE VENDOR: WIN32-X \nCONNECTION TYPE: Ethernet ICMP \nHOPS:192168.0.1 192168.1.1 100.73.43.4host-132.12.32.167.ucom.comhost-66.120.12.111.ucom.com36.134.67.189 216.239.78.111 sof02s32-in-f14.1e100.net \nTOTAL HOPS: 8 \nACTIVESERVICES: [HTTP]192.168.3.1:80=>92.28.211.234:80\n[HTTP]192.168.3.1:443=>92.28.211.234:443\n[UDP] 192.168.0.1:788=>192.168.1:6557\n[TCP]192.168.1.1:67891=>92.28.211.234:345\n[TCP]192.168.52.43:7777=>192.168.1.1:7778\n[TCP]192.168.78.12:898=>192.168.89.9:667\nEXTERNAL",
    f"HAHAHHAHAHAHAHAH {new_name} LMAOOO!!! EVERYONE POINT AND LAUGH AT {victim.mention}",
    f"{victim.mention} is now {new_name} na nite pal,,",
    f"{victim.mention} is now {new_name}, as recompense they get 1 free pass to say whatever word they want!",
    f"hey kid, heard they callin' ya {new_name} now...",
    f"they call you {new_name}.",
    f"im so sick of this shit",
    f"wow yeah... they really DO call you {new_name} thats so true",
    f"you dont have to tell me twice, but during the stone age...",
    f"wow! is that {victim.mention}? no... wait, its {new_name}...",
    f"by the power invested in me i now pronounce you to be {new_name}!",
    f"{victim.mention}, be glad its not..like.. idk, {victim.mention}smells.. or like {victim.mention}isgay or something",
    f"really not appropriate guys is it....",
    f"mfw they call you {new_name}: <:beefstew:1285630081829437614>"
    ]
    
    response = random.choice(responses)
    return response

