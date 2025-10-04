import discord
from data import postgres
import datetime
from beefutilities.guilds.guild_text_channel import read_guild_info_channel
from beefutilities.IO import file_io
import os

async def check_for_holiday(bot):
    print(f"> \033[95mscheduled holiday check ran at {datetime.datetime.now()}\033[0m")

    today = datetime.datetime.now().date()
    holidays = {
        (1, 1): "New Year's Day",
        (25, 12): "Christmas",
        (30, 10): "Halloween"
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
    # give each registered user 10 points for christmas
    await postgres.write(f"UPDATE public.joke_scores SET current_score = current_score + 10 WHERE guild_id = {guild.id} AND user_id != 99;")

    # get all the users in the guild and update their highest score if they have a higher score than before
    users = await postgres.read(f"SELECT * FROM public.joke_scores WHERE guild_id = {guild.id};")
    for user in users:
        user_id = user[0]
        guild_id = user[1]
        score = user[2]
        highest_score = user[3]
        if highest_score < score:
            await postgres.write(f"UPDATE public.joke_scores SET highest_score = {score} WHERE user_id = '{user_id}' AND guild_id = '{guild_id}';")

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
    # give each registered user 5 points for halloween
    await postgres.write(f"UPDATE public.joke_scores SET current_score = current_score + 5 WHERE guild_id = {guild.id} AND user_id != 99;")

    # get all the users in the guild and update their highest score if they have a higher score than before
    users = await postgres.read(f"SELECT * FROM public.joke_scores WHERE guild_id = {guild.id};")
    for user in users:
        user_id = user[0]
        guild_id = user[1]
        score = user[2]
        highest_score = user[3]

        if highest_score < score:
            await postgres.write(f"UPDATE public.joke_scores SET highest_score = {score} WHERE user_id = '{user_id}' AND guild_id = '{guild_id}';")

    # get the info channel for the guild and send the message
    channel = await guild.fetch_channel(await read_guild_info_channel(guild.id))
    await channel.send(
        content="ooOOOOoooOOooo.... BOO! AHHHH im so scared on halloween today!!\n...trick or treat..?\n my beefstew treat... +5 points for u!",
        file=discord.File(fp=file_io.construct_assets_path("stews/halloweenstew.png"), filename="halloweenstew.png")
        )
