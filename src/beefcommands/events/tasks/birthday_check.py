import discord
from data import postgres
import datetime
from beefutilities.guilds.guild_text_channel import read_guild_info_channel
from beefcommands.visage.bday import party_pfp
from beefcommands.invocations.joker_score import read_joker_score, change_joker_score
import os


async def check_for_birthdays(bot):
    print(f"> \033[95mscheduled birthday check ran at {datetime.datetime.now()}\033[0m")

    # read from the db all users with a registered birthday
    users = await postgres.read("SELECT user_id, user_name, birthday FROM users WHERE birthday IS NOT NULL;")
    today = datetime.datetime.now().date()

    # fpr each user found compare it to todays month/day
    for user in users:
        user_id, user_name, birthday = user
        if birthday.month == today.month and birthday.day == today.day:

            # fetch a member object from the guild
            guild = await bot.fetch_guild(os.getenv("GUILDID"))
            user_obj = await guild.fetch_member(user_id)

            channel = bot.get_channel(await read_guild_info_channel(guild.id))

            # making sure the user is registered in the db
            await read_joker_score.retrieve_joke_score(user_obj)

            # give the user 15 poinbts for their birthday
            await postgres.write(f"UPDATE public.joke_scores SET current_score = current_score + 15 WHERE user_id = '{user_id}' AND guild_id = '{guild.id}';")
            await channel.send(content=f"Happy Birthday {user_obj.mention}\n +15 points for u :)", file=discord.File(fp=await party_pfp(user_obj), filename=f"happy bday {user_name}.png"))

            # make sure to update the highest and lowest score for the user
            await change_joker_score.set_highest_score(user_obj, await read_joker_score.retrieve_joke_score(user_obj))
            await change_joker_score.set_lowest_score(user_obj, await read_joker_score.retrieve_joke_score(user_obj))
            return
    return