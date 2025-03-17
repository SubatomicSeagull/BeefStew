import discord
from data import postgres

async def is_registered(user: discord.Member):
    user = await (postgres.read(f"SELECT current_score FROM public.joke_scores WHERE user_id = '{user.id}';"))
    if len(user) == 0:
        return False
    else:
        return True
    
async def register_user(user: discord.Member):
        await postgres.write(f"INSERT INTO public.users(user_id, user_name) VALUES ({user.id}, '{user.global_name}');")
        await postgres.write(f"INSERT INTO public.joke_scores(user_id, guild_id, current_score, highest_score, lowest_score, user_name, user_display_name VALUES ({user.id}, {user.guild.id}, 0, 0, 0, {user.global_name}, {user.nick});")

async def deregister_user(user: discord.Member):  
    await postgres.write(f"DELETE FROM public.users WHERE user_id = {user.id};")