import discord
from data import postgres
from beefutilities.guilds import text_channel

async def is_registered(user: discord.Member):
    # if the guild isnt registered, register it
    if not await text_channel.guild_exists(user.guild.id):
        await text_channel.add_guild(user.guild.id, user.guild.name)
    
    user = await (postgres.read(f"SELECT * FROM public.users WHERE user_id = '{user.id}';"))
    if user == []:
        return False
    else:
        return True
    
async def register_user(user: discord.Member):
    # register the user into the users table
    await postgres.write(f"INSERT INTO public.users(user_id, user_name, msg_flag) VALUES ({user.id}, '{user.global_name}', FALSE);")

    # register the user into the joke_scores table with some default values
    await postgres.write(f"INSERT INTO public.joke_scores(user_id, guild_id, current_score, highest_score, lowest_score, user_name, user_display_name) VALUES ({user.id}, {user.guild.id}, 0, 0, 0, '{user.global_name}', '{user.nick}');")

async def deregister_user(user: discord.Member):  
    await postgres.write(f"DELETE FROM public.users WHERE user_id = {user.id};")