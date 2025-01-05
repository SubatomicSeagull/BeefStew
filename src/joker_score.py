from data import postgres
import discord
from responses import get_joke_response_positive, get_joke_response_negative

async def retrieve_joke_score(user: discord.Member):
    joke_score = await (postgres.read(f"SELECT joke_score FROM user_joker_score WHERE user_id = '{user.id}';"))
    score = joke_score[0][0]
    return int(score)
    
async def change_joke_score(self: discord.Member, user: discord.Member, value):
    if self.id == user.id and value > 0:
        return "cant do that lol lmao loser"
    elif self.id == user.id and value < 0:
        await postgres.write(f"UPDATE user_joker_score SET joke_score = joke_score + {value} WHERE user_id = '{user.id}';")
        await postgres.write(f"UPDATE user_joker_score SET member_name = '{user.nick}' WHERE user_id = '{user.id}';")
        return f"{self.mention} -2'd themselves for some reason... oh well!\n {await get_joke_response_negative(user)}"
    
    if not await is_registered(user):
        await register_user(user)
    try:
        mult = await get_multilplier(user)
        score = value * mult
        await postgres.write(f"UPDATE user_joker_score SET joke_score = joke_score + {score} WHERE user_id = '{user.id}';")
        await postgres.write(f"UPDATE user_joker_score SET member_name = '{user.nick}' WHERE user_id = '{user.id}';")
        if score > 0: 
            return (await get_joke_response_positive(user))
        else:
            return (await get_joke_response_negative(user))
    except Exception as e:
        await postgres.log_error(e)
        return (f"couldnt change score for {user.name} :( ({e}))")

async def clear_joke_score(user: discord.Member):
    await postgres.write(f"UPDATE user_joker_score SET joke_score = 0 WHERE user_id = '{user.id}';")

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

async def get_multilplier(user: discord.Member):
    winner = discord.utils.get(user.guild.roles, name="the funniest person ever")
    loser = discord.utils.get(user.guild.roles, name="tonights biggest loser")   
    if winner in user.roles:
        return 1.5
    elif loser in user.roles:
        return 0
    else:
        return 1