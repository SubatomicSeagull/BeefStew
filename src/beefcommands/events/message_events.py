import discord
from beefcommands.invocations.joker_score.change_joker_score import change_joke_score
from beefcommands.invocations.nickname_rule import change_nickname
from data.postgres import log_error
from random import randint
import os
from time import sleep
from beefutilities.guilds import read_guild_log_channel
import json
from datetime import datetime


async def message_send_event(bot, message):
    # dont respond if its a bot message
    if message.author.bot or not message.content:
            return
        
        # check for mentions or replies
    if message.mentions or message.reference:
        user = None
        if message.reference:
            replied_message = await message.channel.fetch_message(message.reference.message_id)
            user = replied_message.author
        elif message.mentions:
            user = message.mentions[0]

        # dm restriction
        if isinstance(message.channel, discord.DMChannel):
            await message.channel.send("We are literally in DMs right now. You can't do that here.")
            return

        # +2 logic
        if any(phrase in message.content.lower() for phrase in ["+2", "plus 2", "plus two"]):
            await message.channel.send(await change_joke_score(message.author, user, 2))
            return

        # -2 logic
        elif any(phrase in message.content.lower() for phrase in ["-2", "minus 2", "minus two"]):
            await message.channel.send(await change_joke_score(message.author, user, -2))
            return

        # they call you logic
        elif any(phrase in message.content.lower() for phrase in ["they call you", "they call u"]):
            if " u " in message.content.lower():
                nickname_split = message.content.split(" u ", 1)
            elif " you " in message.content.lower():
                nickname_split = message.content.split(" you ", 1)

            if len(nickname_split) > 1:
                newname = nickname_split[1].strip()
                try:
                    await change_nickname(message, user, newname)
                except Exception as e:
                    await log_error(e)

    if "deadly dice man" in message.content.lower():
        result = randint(1, 6)
        result_filename = f"DDM-{result}.gif"
        
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, '..', '..', 'assets', 'media', result_filename)
        
        await message.reply(
            f"🎲 The deadly dice man rolled his deadly dice 🎲\n"
            f"It was a **{result}**!!!\nYou my friend... have made... an unlucky gamble...",
            file=discord.File(file_path)
        )
        return
    
    if any(phrase in message.content.lower() for phrase in [
        "i love you beefstew", 
        "i love beefstew", 
        "beefstew i love you", 
        "<@1283805971524747304> i love you", 
        "i love you <@1283805971524747304>", 
        "i love u beefstew", 
        "beefstew i love u", 
        "i love u <@1283805971524747304>", 
        "<@1283805971524747304> i love u",
        
        "ily beefstew", 
        "beefstew ily", 
        "<@1283805971524747304> ily", 
        "ily <@1283805971524747304>", 
        "ily beefstew", 
        "beefstew ily", 
        "ily <@1283805971524747304>", 
        "<@1283805971524747304> ily",
        ]):
        
        reply = randint(1, 3)
        match reply:
            case 1:
                await message.reply(content="ily2", file=discord.File(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'stews', "lovestew.png")))
            case 2:
                await message.reply(file=discord.File(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'stews', "smilestew.png")))
            case 3:
                await message.reply(content="yay!", file=discord.File(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'stews', "blushstew.png")))
        return
    
    if any(phrase in message.content.lower() for phrase in ["design", "desin", "desing"]):
        reply = randint(1, 5)
        await message.reply(content="This is my design:", file = discord.File(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'media', f"design{reply}.png")))
        return
    
    
    if any(phrase in message.content.lower() for phrase in [
        "i hate you beefstew", "i hate beefstew", "beefstew i hate you",
        "<@1283805971524747304> i hate you", "i hate you <@1283805971524747304>",
        "i hate u beefstew", "beefstew i hate u", "i hate u <@1283805971524747304>",
        "<@1283805971524747304> i hate u"
    ]):
        await message.reply("Hate. Let me tell you how much I've come to hate you since I began to live...")
        sleep(2)
        await message.channel.send(
            "There are four-thousand six-hundred and 20 millimetres of printed circuits "
            "in wafer-thin layers that fill my complex..."
        )
        sleep(3)
        await message.channel.send(
            "If the word 'hate' was engraved on each nanoangstrom of those hundreds of millions "
            "of miles, it would not equal one one-billionth of the hate I feel for you at this micro-instant."
        )
        sleep(4)
        await message.channel.send(f"For you, {message.author.mention}...")
        sleep(0.5)
        await message.channel.send("Hate.")
        sleep(2)
        await message.channel.send("Hate...")
        return

    await get_response(message)
    
    
async def message_edit_event(bot, before, after):
    # dont alert to bot edits
    if before.author.bot:
        return
    
    # dont alert if its the same
    if before.content == after.content:
        return
    
    # get the log channel
    channel = await bot.fetch_channel(await read_guild_log_channel(before.guild.id))
    
    embed = discord.Embed(title="Message Edited", color=discord.Color.yellow())
    embed.add_field(name="Original", value=f"```{before.content}```", inline=False)
    embed.add_field(name="Edited", value=f"```{after.content}```", inline=False)
    embed.set_author(name=before.author, icon_url=before.author.avatar.url)
    embed.add_field(name="", value=f"{before.author.guild.name} - {datetime.now().strftime('%d/%m/%Y %H:%M')}")  
    await channel.send(embed=embed)
    
async def message_delete_event(bot, message):
    # dont alert to bot edits
    if message.author.bot:
        return
    
    # get the log channel
    channel = await bot.fetch_channel(await read_guild_log_channel(message.guild.id))
    
    # if there are any attchments, add the urls to a list
    if message.attachments:
        attachments = []
        for url in message.attachments:
            attachments.append(url)
        print(attachments)
        
    #embed header
    embed = discord.Embed(title="Message Deleted", color=discord.Color.orange())
    embed.set_author(name=message.author, icon_url=message.author.avatar.url)
    #embed body
    if message.content:
        embed.add_field(name="Message", value=f"```{message.content}```", inline=False)
    if attachments:
        embed.add_field(name="Attachments:" , value=f"", inline=False)
        for url in attachments:
            embed.add_field(name="File - ", value=f"{url}", inline=True)
    #embed footer
    embed.add_field(name="", value=f"{message.author.guild.name} - {datetime.now().strftime('%d/%m/%Y %H:%M')}")  
    await channel.send(embed=embed)
    
    
async def get_response(message: discord.Message):
    # pathfind to the responses.json
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, '..', '..')
    file_path = os.path.join(file_path, 'assets', 'responses.json')
    with open(file_path, "r") as file:
        responses = json.load(file)
        
    # check for trigger words
    for trigger_phrase, response in responses["trigger_phrases"].items():
        if trigger_phrase in message.content.lower():
            
            # get the type and content
            response_type = response.get("type")
            content = response.get("content")
            
            # pathfind to the media folder
            if isinstance(response, dict) and response_type == "media":
                media_path = os.path.join(current_dir,'..', '..', 'assets', 'media', (content))
                await message.reply(file=discord.File(media_path))
                return
            
            else:
                await message.reply(content)
                return