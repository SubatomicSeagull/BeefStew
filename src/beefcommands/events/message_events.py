import discord
from beefcommands.invocations.joker_score.change_joker_score import change_joke_score, hawk_tuah_penalty
from beefcommands.invocations.nickname_rule import change_nickname
from beefcommands.utilities.music_player.youtube import yt_utils
from data.postgres import log_error
from random import randint
from time import sleep
from beefutilities.guilds.text_channel import read_guild_log_channel
import beefcommands.invocations.channel_name_rule as channel_name_rule
from beefcommands.utilities.showme import show
from beefcommands.utilities.tellme import tellme

import json
from datetime import datetime
from beefutilities.IO import file_io


async def message_send_event(bot, message):
    # dont respond if its a bot message
    if message.author.bot or not message.content:
            return
        
    if "/say" in message.content.lower():
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
        
        file_path = file_io.construct_media_path(result_filename)
        
        await message.reply(
            f"🎲 The deadly dice man rolled his deadly dice 🎲\n"
            f"It was a **{result}**!!!\nYou my friend... have made... an unlucky gamble...",
            file=discord.File(file_path)
        )
        return
    
    if any(phrase in message.content.lower() for phrase in [
        "beefstew show me", "<@1283805971524747304> show me"    
    ]):
        show_split = message.content.split("show me ", 1)
        await show(message, show_split[1])
        
    if any(phrase in message.content.lower() for phrase in [
        "beefstew tell me about", "<@1283805971524747304> tell me about",
        "beefstew what is", "<@1283805971524747304> what is",
        "beefstew whats", "<@1283805971524747304> whats",
        "beefstew what's", "<@1283805971524747304> what's",
        "beefstew what are", "<@1283805971524747304> what are",
        "beefstew what're", "<@1283805971524747304> what're"
    ]):
        lower_content = message.content.lower()
        for phrase in [
            "tell me about", "what is", "whats", "what's", "what are", "what're"
        ]:
            if phrase in lower_content:
                tell_split = lower_content.split(phrase, 1)
                if len(tell_split) > 1:
                    query = tell_split[1].strip()
                    await tellme(message, query)

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
                await message.reply(content="ily2", file=discord.File(file_io.construct_assets_path("stews/lovestew.png")))
                
            case 2:
                await message.reply(file=discord.File(file_io.construct_assets_path("stews/smilestew.png")))
            case 3:
                await message.reply(content="yay!", file=discord.File(file_io.construct_assets_path("stews/blushstew.png")))
        return
    
    if any(phrase in message.content.lower() for phrase in ["design", "desin", "desing"]):
        reply = randint(1, 6)
        await message.reply(content="This is my design:", file = discord.File(file_io.construct_media_path(f"design{reply}.png")))

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


    if "new kay" in message.content.lower():
        kayupdate = await message.channel.send(content= "checking for new kay video...", file=None)
        name, url, title = await yt_utils.find_newest_yt_video("https://www.youtube.com/@KaysCooking")
        file = discord.File(file_io.construct_media_path("newkay.gif"))
        await kayupdate.delete()
        await message.channel.send(content=f"guys new kay video... **[{title}](https://www.youtube.com/watch?v={url})**", file=file)
        return
    
    if "crazy" in message.content.lower():
        await message.channel.send("Crazy...?")
        sleep(1)
        await message.channel.send("I was crazy once...")
        sleep(0.5)
        await message.channel.send("They locked me in a room with rubber rats")
        sleep(0.5)
        await message.channel.send("And the rubber rats made me go crazy!!!!!!!!!!!!!!!!!")
        return
        
    if "tuah" in message.content.lower():
        jar_total = await hawk_tuah_penalty(message.author)
        file = discord.File(file_io.construct_media_path("hawktuahjar.gif"))
        await message.reply(content=f"{message.author.mention} pays the Hawk Tuah Penalty!!! Another 2 points to the jar...\n**Jar Points: {jar_total}**", file=file)
        return
    
    if "why are we in " or "we are in " in message.content.lower():
        channel_name_split = message.content.split(" in ", 1)
        if len(channel_name_split) > 1:
            newname = channel_name_split[1].strip()
            await channel_name_rule.invoke_channel_name_rule(message, newname)
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
    
    embed = discord.Embed(title=f"Message Edited in {channel.mention}", color=discord.Color.yellow())
    embed.add_field(name="Original", value=f"```{before.content}```", inline=False)
    embed.add_field(name="Edited", value=f"```{after.content}```", inline=False)
    embed.set_author(name=before.author, icon_url=before.author.avatar.url)
    embed.add_field(name="", value=f"{before.author.guild.name} - {datetime.now().strftime('%d/%m/%Y %H:%M')}")  
    await channel.send(embed=embed)
    
async def message_delete_event(bot, message):
    # dont alert to bot edits
    if message.author.bot:
        return
    
    # dont send an embed if its through the /say command
    if "/say" in message.content.lower():
        return
    
    # get the log channel
    channel = await bot.fetch_channel(await read_guild_log_channel(message.guild.id))
    
    # if there are any attchments, add the urls to a list
    if message.attachments:
        attachments = []
        for url in message.attachments:
            attachments.append(url)
    else: attachments = None
    print(attachments)
        
    #embed header
    embed = discord.Embed(title=f"Message Deleted in {channel.mention}", color=discord.Color.orange())
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
    file_path = file_io.construct_assets_path('responses.json')
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
                media_path = file_io.construct_media_path(content)
                await message.reply(file=discord.File(media_path))
                return
            
            else:
                await message.reply(content)
                return