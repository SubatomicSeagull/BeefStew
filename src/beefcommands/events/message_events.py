import re
import discord
from beefcommands.invocations.joker_score.change_joker_score import change_joke_score, hawk_tuah_penalty
from beefcommands.invocations.nickname_rule import change_nickname
from beefcommands.utilities.show_me import show
from beefutilities import yt_utils
from data.postgres import log_error
from random import randint
from time import sleep
from beefutilities.guilds.guild_text_channel import read_guild_log_channel
import beefcommands.invocations.channel_name_rule as channel_name_rule
from beefutilities import TTS
from beefcommands.utilities.tell_me import tell_me
from beefutilities.TTS import speak
import json
from datetime import datetime
from beefutilities.IO import file_io

async def message_send_event(bot: discord.Client, message: discord.Message):
    # dont respond if its a bot message
    if message.author.bot or not message.content:
        return

    # dont respond to links
    if message.content.lower().startswith("http"):
        return

    # dont respond to /say command messages
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
            response = await change_joke_score(message.author, user, 2, message.content)
            await message.channel.send(response)
            await TTS.speak_output(message, response)
            return

        # -2 logic
        elif any(phrase in message.content.lower() for phrase in ["-2", "minus 2", "minus two"]):
            response = await change_joke_score(message.author, user, -2, message.content)
            await message.channel.send(response)
            await TTS.speak_output(message, response)
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
                    await change_nickname(message, user, newname, False)
                except Exception as e:
                    await log_error(e)

    if any(phrase in message.content.lower() for phrase in ["they call me"]):
        if " me " in message.content.lower():
            nickname_split = message.content.split(" me ", 1)

        if len(nickname_split) > 1:
            newname = nickname_split[1].strip()
            try:
                await change_nickname(message, message.author, newname, True)
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
        await TTS.speak_output(message, f"The deadly dice man rolled his deadly dice... it was a {result}!!! You my friend... have made... an unlucky gamble...")
        return

    if any(phrase in message.content.lower() for phrase in [
        "beefstew show me", "<@1283805971524747304> show me"
    ]):
        show_split = message.content.split("show me ", 1)
        await show(message, show_split[1])

    pattern = re.compile(
        r"(?:beefstew|<@1283805971524747304>)\s+(?:tell me about|what is|whats|what's|what are|what're)\s+(.+)",
        re.IGNORECASE
    )

    match = pattern.search(message.content.strip())
    if match:
        query = match.group(1).strip()
        if query:
            await tell_me(message, query)

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

        reply = randint(1, 4)
        match reply:
            case 1:
                await message.reply(content="ily2", file=discord.File(file_io.construct_assets_path("stews/lovestew.png")))
                await TTS.speak_output(message, "ILY 2")

            case 2:
                await message.reply(file=discord.File(file_io.construct_assets_path("stews/smilestew.png")))
            case 3:
                await message.reply(content="yay!", file=discord.File(file_io.construct_assets_path("stews/blushstew.png")))
                await TTS.speak_output(message, "Yay!")
        return

    if any(phrase in message.content.lower() for phrase in ["design", "desin", "desing"]):
        reply = randint(1, 6)
        await message.reply(content="This is my design:", file = discord.File(file_io.construct_media_path(f"design{reply}.png")))
        await TTS.speak_output(message, "This... is my design.")
        return


    if any(phrase in message.content.lower() for phrase in [
        "i hate you beefstew", "i hate beefstew", "beefstew i hate you",
        "<@1283805971524747304> i hate you", "i hate you <@1283805971524747304>",
        "i hate u beefstew", "beefstew i hate u", "i hate u <@1283805971524747304>",
        "<@1283805971524747304> i hate u"
    ]):
        await message.reply("Hate. Let me tell you how much I've come to hate you since I began to live...")
        if message.author.nick:
            await TTS.speak_output(message, f"Hate. Let me tell you how much I've come to hate you since I began to live. \nThere are four-thousand six-hundred and 20 millimetres of printed circuits. \nIn wafer-thin layers that fill my complex. If the word 'hate' was engraved on each nanoangstrom of those hundreds of millions of miles, it would not equal one one-billionth of the hate I feel for you at this micro-instant. \nFor you, {message.author.nick}. \n Hate.")
        else:
            await TTS.speak_output(message, f"Hate. Let me tell you how much I've come to hate you since I began to live. \nThere are four-thousand six-hundred and 20 millimetres of printed circuits. \nIn wafer-thin layers that fill my complex. If the word 'hate' was engraved on each nanoangstrom of those hundreds of millions of miles, it would not equal one one-billionth of the hate I feel for you at this micro-instant. \nFor you, {message.author.name}. \n Hate.")
        
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
        await TTS.speak_output(message, f"Guys new kay video...\n {title}")
        return

    if "crazy" in message.content.lower():
        await message.channel.send("Crazy...?")
        sleep(1)
        await message.channel.send("I was crazy once...")
        sleep(0.5)
        await message.channel.send("They locked me in a room with rubber rats")
        sleep(0.5)
        await message.channel.send("And the rubber rats made me go crazy!!!!!!!!!!!!!!!!!")
        await TTS.speak_output(message, "Crazy...? I was crazy once... They locked me in a room with rubber rats and the rubber rats made me go crazy!")
        return

    if "tuah" in message.content.lower():
        jar_total = await hawk_tuah_penalty(message.author)
        file = discord.File(file_io.construct_media_path("hawktuahjar.gif"))
        await message.reply(content=f"{message.author.mention} pays the Hawk Tuah Penalty!!! Another 2 points to the jar...\n**Jar Points: {jar_total}**", file=file)
        
        if message.author.nick:
            await TTS.speak_output(message, f"{message.author.nick} pays the Hawk Tuah Penalty!!! Another 2 points to the jar...")
        else:
            await TTS.speak_output(message, f"{message.author.name} pays the Hawk Tuah Penalty!!! Another 2 points to the jar...")
        return

    if any(phrase in message.content.lower() for phrase in ["why are we in ", "we are in "]):
        channel_name_split = message.content.split(" in ", 1)
        if len(channel_name_split) > 1:
            newname = channel_name_split[1].strip()
            await channel_name_rule.invoke_channel_name_rule(message, newname)
            return

    await get_response(message)

async def message_edit_event(bot: discord.Client, before, after):
    # dont alert to bot edits
    if before.author.bot:
        return

    # dont alert if its the same
    if before.content == after.content:
        return


    # get the log channel
    channel = await bot.fetch_channel(await read_guild_log_channel(before.guild.id))

    embed = discord.Embed(title=f"Message Edited in {before.channel.mention}", color=discord.Color.yellow())
    embed.add_field(name="Original", value=f"```{before.content}```", inline=False)
    embed.add_field(name="Edited", value=f"```{after.content}```", inline=False)
    embed.set_author(name=before.author, icon_url=before.author.avatar.url)
    embed.add_field(name="", value=f"{before.author.guild.name} - {datetime.now().strftime('%d/%m/%Y - %H:%M')}")
    await channel.send(embed=embed)

async def message_delete_event(bot: discord.Client, message: discord.Message):
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
    embed = discord.Embed(title=f"Message Deleted in {message.channel.mention}", color=discord.Color.orange())
    embed.set_author(name=message.author, icon_url=message.author.avatar.url)
    #embed body
    if message.content:
        embed.add_field(name="Message", value=f"```{message.content}```", inline=False)
    if attachments:
        embed.add_field(name="Attachments:" , value=f"", inline=False)
        for url in attachments:
            embed.add_field(name="File - ", value=f"{url}", inline=False)
    #embed footer
    embed.add_field(name="", value=f"{message.author.guild.name} - {datetime.now().strftime('%d/%m/%Y - %H:%M')}")
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
                await TTS.speak_output(message, content)
                return


