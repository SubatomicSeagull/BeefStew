import discord
from data import postgres
import datetime
from beefutilities.guilds.text_channel import read_guild_info_channel
from beefutilities.IO import file_io

async def check_for_holiday(bot):
    print(f"> \033[95mscheduled holiday check ran at {datetime.datetime.now()}\033[0m")
    today = datetime.datetime.now().date()
    holidays = {
        (29, 3): "New Year's Day",
        (12, 25): "Christmas",
        (10, 31): "Halloween"
    }
    guild_id = 1015579904005386250
    channel = bot.get_channel(await read_guild_info_channel(guild_id))
    
    for date, holiday_name in holidays.items():
        if date == (today.month, today.day):
            if holiday_name == "New Year's Day":
                await new_years_event(channel)
            elif holiday_name == "Christmas":
                await christmas_event(channel, guild_id)
            elif holiday_name == "Halloween":
                await halloween_event(channel, guild_id)
                

async def christmas_event(channel, guild_id):
    #await postgres.write(f"UPDATE public.joke_scores SET current_score = current_score + 10 WHERE guild_id = {guild_id};")
    await channel.send(
        content="# 🎄HAPPY BEEFMAS!! 🎄\nWHat has ol' st. stew claus brought u...\n ho ho ho 10 points to everyone!", 
        file=discord.File(fp=file_io.construct_assets_path("stews/chistmasstew.png"), filename="christmasstew.png")
        )

async def new_years_event(channel):
    await channel.send(
        content=f"# 🎇HNY {datetime.datetime.now().date().year} 🎇", 
        file=discord.File(fp=file_io.construct_assets_path("stews/nyestew.png"), filename="newyearsstew.png")
        )

async def halloween_event(channel, guild_id):
    #await postgres.write(f"UPDATE public.joke_scores SET current_score = current_score + 5 WHERE guild_id = {guild_id};")
    await channel.send(
        content="ooOOOOoooOOooo.... BOO! AHHHH im so scared on halloween today!!\n...trick or treat..?\n my beefstew treat +5 points for u!", 
        file=discord.File(fp=file_io.construct_assets_path("stews/halloweenstew.png"), filename="halloweenstew.png")
        )
