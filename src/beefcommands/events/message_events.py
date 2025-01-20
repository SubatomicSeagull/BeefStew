import discord
from beefcommands.invocations.joker_score.change_joker_score import change_joke_score
from beefcommands.invocations.nickname_rule import change_nickname
from data.postgres import log_error
from random import randint
import os
from time import sleep
from beefutilities.guilds import read_guild_log_channel
import json


async def message_send_event(bot, message):
    if message.author.bot or not message.content:
            return
        # Check for mentions or references
    if message.mentions or message.reference:
        user = None
        if message.reference:
            replied_message = await message.channel.fetch_message(message.reference.message_id)
            user = replied_message.author
        elif message.mentions:
            user = message.mentions[0]

        # DM Channel Restriction
        if isinstance(message.channel, discord.DMChannel):
            await message.channel.send("We are literally in DMs right now. You can't do that here.")
            return

        # "+2" or "-2" Logic
        if any(phrase in message.content.lower() for phrase in ["+2", "plus 2", "plus two"]):
            await message.channel.send(await change_joke_score(message.author, user, 2))
            return

        elif any(phrase in message.content.lower() for phrase in ["-2", "minus 2", "minus two"]):
            await message.channel.send(await change_joke_score(message.author, user, -2))
            return

        # Nickname Change Logic
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

    # "Deadly Dice Man" Logic
    if "deadly dice man" in message.content.lower():
        result = randint(1, 6)
        result_filename = f"DDM-{result}.gif"
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, 'assets', 'media', result_filename)
        await message.reply(
            f"🎲 The deadly dice man rolled his deadly dice 🎲\n"
            f"It was a **{result}**!!!\nYou my friend... have made... an unlucky gamble...",
            file=discord.File(file_path)
        )
        return

    # "Hate Message" Response
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
    await bot.process_commands(message)
    
    
async def message_edit_event(bot, before, after):
    if before.author == bot.user:
        return
    channel = await bot.fetch_channel(await read_guild_log_channel(before.guild.id))
    embed = discord.Embed(title="Message Edited", color=discord.Color.yellow())
    embed.add_field(name="Original", value=f"```{before.content}```", inline=False)
    embed.add_field(name="Edited", value=f"```{after.content}```", inline=False)
    embed.set_author(name="Beefstew", icon_url=bot.user.avatar.url)
    await channel.send(embed=embed)
    
async def message_delete_event(bot, message):
    if message.author == bot.user:
        return
    channel = await bot.fetch_channel(await read_guild_log_channel(message.guild.id))
    embed = discord.Embed(title="Message Deleted", color=discord.Color.orange())
    embed.add_field(name="Message", value=f"```{message.content}```", inline=False)
    embed.set_author(name="Beefstew", icon_url=bot.user.avatar.url)
    await channel.send(embed=embed)
    
    
async def get_response(message: discord.Message):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'assets', 'responses.json')
    with open(file_path, "r") as file:
        responses = json.load(file)
    for trigger_phrase, response in responses["trigger_phrases"].items():
        if trigger_phrase in message.content.lower():
            response_type = response.get("type")
            content = response.get("content")
            if isinstance(response, dict) and response_type == "media":
                media_path = os.path.join(current_dir, 'assets', 'media', (content))
                await message.reply(file=discord.File(media_path))
                return
            else:
                await message.reply(content)
                return