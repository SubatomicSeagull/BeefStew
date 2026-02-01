import discord
from data import postgres
import datetime
from beefutilities.guilds.guild_text_channel import read_guild_info_channel
from beefutilities.IO import file_io
import os
from beefcommands.invocations.joker_score.change_joker_score import change_joke_score

async def check_for_holiday(bot: discord.Client):
    print(f"> \033[95mscheduled holiday check ran at {datetime.datetime.now()}\033[0m")

    today = datetime.datetime.now().date()
    holidays = {
        (1, 1): "New Year's Day",
        (25, 12): "Christmas",
        (31, 10): "Halloween"
    }

    # fetch the guild object from the guild id
    guild = await bot.fetch_guild(os.getenv("GUILDID"))

    # compare the current date to the holidays list
    for date, holiday_name in holidays.items():
        print(f"checking {date} against {today.day, today.month}")
        if date == (today.day, today.month):
            if holiday_name == "New Year's Day":
                await new_years_event(guild)
                return
            elif holiday_name == "Christmas":
                await christmas_event(guild)
                return
            elif holiday_name == "Halloween":
                await halloween_event(guild)
                return

async def christmas_event(guild: discord.Guild):
    users = await postgres.read(f"SELECT user_id FROM public.joke_scores WHERE guild_id = {guild.id};")
    for user in users:
        try:
            uid = int(user[0])
            botuser = await guild.fetch_member(os.getenv("CLIENTID"))
            user_obj = await guild.fetch_member(uid)
            if uid != 99 and uid != os.getenv("CLIENTID"):
                await change_joke_score(botuser , user_obj, 10, "christmas present")
        except discord.NotFound:
            continue

    # get the info channel for the guild and send the message
    channel = await guild.fetch_channel(await read_guild_info_channel(guild.id))

    await channel.send(
        content="# 🎄HAPPY BEEFMAS!! 🎄\nwhat has ol' st. stew brought u...\n ho ho ho 10 points to everyone!",
        file=discord.File(fp=file_io.construct_assets_path("stews/christmasstew.png"), filename="christmasstew.png")
        )

async def new_years_event(guild: discord.Guild):
    channel = await guild.fetch_channel(await read_guild_info_channel(guild.id))
    await channel.send(
        content=f"# 🎇 HNY {datetime.datetime.now().date().year}!!! 🎇",
        file=discord.File(fp=file_io.construct_assets_path("stews/nyestew.png"), filename="newyearsstew.png")
        )

async def halloween_event(guild: discord.Guild):
    users = await postgres.read(f"SELECT user_id FROM public.joke_scores WHERE guild_id = {guild.id};")
    for user in users:
        try:
            uid = int(user[0])
            botuser = await guild.fetch_member(os.getenv("CLIENTID"))
            user_obj = await guild.fetch_member(uid)
            if uid != 99 and uid != os.getenv("CLIENTID"):
                await change_joke_score(botuser , user_obj, 5, "haloween treat")
        except discord.NotFound:
            continue
    # get the info channel for the guild and send the message
    channel = await guild.fetch_channel(await read_guild_info_channel(guild.id))
    await channel.send(
        content="ooOOOOoooOOooo.... BOO! AHHHH im so scared on halloween today!!\n...trick or treat..?\n my beefstew treat... +5 points for u!",
        file=discord.File(fp=file_io.construct_assets_path("stews/halloweenstew.png"), filename="halloweenstew.png")
        )
