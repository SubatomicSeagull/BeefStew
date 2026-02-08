import discord
from data import postgres
from beefutilities.guilds import guild_text_channel

async def is_registered_users(user: discord.Member):
    # if the guild isnt registered, register it
    if not await guild_text_channel.guild_exists(user.guild.id):
        await guild_text_channel.add_guild(user.guild.id, user.guild.name)

    # if the user isnt registered, register them
    user = await (postgres.read(f"SELECT * FROM public.users WHERE user_id = '{user.id}';"))
    if user == []:
        return False
    else:
        return True

async def is_registered_score(user: discord.Member):
    # if the guild isnt registered, register it
    if not await guild_text_channel.guild_exists(user.guild.id):
        await guild_text_channel.add_guild(user.guild.id, user.guild.name)

    # if the user isnt registered, register them
    score = await (postgres.read(f"SELECT * FROM public.joke_scores WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';"))
    if score == []:
        return False
    else:
        return True

async def register_user(user: discord.Member):
    # register the user into the users table
    if user.display_name != None:
        await postgres.write(f"INSERT INTO public.users(user_id, user_name, msg_flag) VALUES ({user.id}, '{user.display_name}', FALSE);")
    else:
        await postgres.write(f"INSERT INTO public.users(user_id, user_name, msg_flag) VALUES ({user.id}, '{user.name}', FALSE);")

async def register_score(user: discord.Member):
    # register the user into the joke_scores table with some default values
    if user.display_name:
        await postgres.write(f"INSERT INTO public.joke_scores(user_id, guild_id, current_score, highest_score, lowest_score, user_name, user_display_name) VALUES ({user.id}, {user.guild.id}, 0, 0, 0, '{user.display_name}', '{user.nick}');")
    else:
        await postgres.write(f"INSERT INTO public.joke_scores(user_id, guild_id, current_score, highest_score, lowest_score, user_name, user_display_name) VALUES ({user.id}, {user.guild.id}, 0, 0, 0, '{user.name}', '{user.nick}');")


async def deregister_user(user: discord.Member):
    await postgres.write(f"DELETE FROM public.joke_scores WHERE user_id = {user.id} AND guild_id = {user.guild.id};")
    await postgres.write(f"DELETE FROM public.users WHERE user_id = {user.id};")