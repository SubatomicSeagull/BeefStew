import random
import asyncio
import discord
import os
from data import postgres
from beefutilities.guilds.guild_text_channel import read_guild_info_channel
from beefcommands.incantations.vicious_mockery import get_insult
from beefutilities.IO.json_handling import load_element

async def random_swing_check(bot):
    # 1/100 chance for the swing to happen
        swing_chance = random.randint(1, 100)
        print(f"Swing chance: {swing_chance}")
        if swing_chance == 1:
            # wait a random number of minutes before proceeding
            delay_minutes = random.randint(1, 56)
            print(f"Delaying swing for {delay_minutes} minutes")
            await asyncio.sleep(delay_minutes * 60)

            # determine the type of swing
            swing_type = random.choices(["insult", "neutral", "image"], weights=[1, 3, 0])[0]

            # determine the channel type
            channel_type = random.choices(["info_channel", "dm"], weights=[1, 3])[0]

            # read flagged users from the db
            flagged_users = await postgres.read("SELECT user_id FROM users WHERE msg_flag = TRUE;")
            if not flagged_users:
                return

            print(f"Flagged users: {flagged_users}")
            # Pick a random user
            user_id = random.choice(flagged_users)[0]

            await send_swing(bot, user_id, swing_type, channel_type)
        return

async def send_swing(bot, user_id, swing_type, channel_type):
    # get the user object
    user = await bot.fetch_user(user_id)
    guild = await bot.fetch_guild(os.getenv("GUILDID"))
    print(f"Swinging at user {user.name} with type {swing_type} in {channel_type}")
    # get the channel object
    swing = ""
    if channel_type == "info_channel":
        swing = (f"{user.mention} ")
        channel = await guild.fetch_channel(await read_guild_info_channel(guild.id))
    else:
        channel = await bot.fetch_channel(user.dm_channel.id) if user.dm_channel else await user.create_dm()

    # send the swing
    if swing_type == "insult":
        await channel.send(content=(swing + await send_insult_swing()))
        return
    elif swing_type == "neutral":
        print("response:")
        await channel.send(content=(swing + await send_neutral_swing()))
        print("done")
        return
    elif swing_type == "image":
        await channel.send(f"image to {user.mention}")
    return

async def send_insult_swing():
    return await get_insult()

async def send_neutral_swing():
    print("picking from responses.json")
    responses = load_element("responses.json", "greetings")
    random_response = random.choice(responses)
    print(random_response)
    return random_response

async def send_image_swing():
    pass