import discord
from data import postgres
import datetime
from beefutilities.guilds.text_channel import read_guild_info_channel
from beefcommands.visage.bday import party_pfp
from beefcommands.invocations.joker_score import read_joker_score, change_joker_score


async def check_for_birthdays(bot):
    print(f"> \033[95mscheduled birthday check ran at {datetime.datetime.now()}\033[0m")
    users = await postgres.read("SELECT user_id, user_name, birthday FROM users WHERE birthday IS NOT NULL;")
    today = datetime.datetime.now().date()
    for user in users:
        user_id, user_name, birthday = user
        # Check if the birthday's month and day match today's month and day
        if birthday.month == today.month and birthday.day == today.day:
            user_obj = bot.get_user(user_id)
            guild_id = 1015579904005386250
            channel = bot.get_channel(await read_guild_info_channel(guild_id))
            await postgres.write(f"UPDATE public.joke_scores SET current_score = current_score + 15 WHERE user_id = '{user_id}' AND guild_id = '{guild_id}';")
            await channel.send(content=f"Happy Birthday {user_obj.mention}\n +15 points for u :)", file=discord.File(fp=await party_pfp(user_obj), filename=f"happy bday {user_name}.png"))
            await change_joker_score.set_highest_score(user, await read_joker_score.retrieve_joke_score(user))
            await change_joker_score.set_lowest_score(user, await read_joker_score.retrieve_joke_score(user))