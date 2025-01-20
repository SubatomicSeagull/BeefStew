import discord
from data import postgres

async def is_registered(user: discord.Member):
    user = await (postgres.read(f"SELECT joke_score FROM user_joker_score WHERE user_id = '{user.id}';"))
    if len(user) == 0:
        return False
    else:
        return True
    
async def register_user(user: discord.Member):
        await postgres.write(f"INSERT INTO public.user_joker_score(user_id, user_name, member_name, joke_score) VALUES ({user.id}, '{user.global_name}', '{user.nick}', {0});")

async def deregister_user(user: discord.Member):  
     await postgres.write(f"DELETE FROM user_joker_score WHERE user_id = {user.id};")