from data import postgres
import discord
import asyncio

# keeps track of a users individual joke score
# joke score is added or taken away through either a /+2 /-2 command with the person they are scoring as an argument,
# or when someone replies to a message with +2 or -2,


#todo
# find a way to store each users individual score
# make it so that they cant adjust their own score
# make it so that they cant adjust beefstew's score
# sanitisation for slash command arguments, is the person they pinged a real user?
# add a way to see a users current score
# add a collection of phrases to say when the score is adjusted
# needs functionaliy to check the person who's message was replied to

#both the reply and slash command should invoke the same code

async def retrieve_joke_score(user: discord.Member):
    joke_score = await (postgres.read(f"SELECT joke_score FROM user_joker_score WHERE user_id = '{user.id}';"))
    score = joke_score[0][0]
    return int(score)
    
async def increment_joke_score(user: discord.Member, value, multiplier):
    score = value * multiplier
    await postgres.write(f"UPDATE user_joker_score SET joke_score = joke_score + {score} WHERE user_id = '{user.id}';")

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