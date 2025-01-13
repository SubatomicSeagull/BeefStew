from data import postgres
import discord
from responses import get_joke_response_positive, get_joke_response_negative
from random import randint

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
    
async def gamble_points(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer()
    #payment
    
    score = await postgres.read(f"SELECT joke_score FROM user_joker_score WHERE user_id = '{user.id}';")
    score = score[0][0]
    
    if score - 2 < 0:
        await interaction.followup.send(f"{user.mention} lmaooo ur broke sry no gambling for u loser")
        return
        
    await postgres.write(f"UPDATE user_joker_score SET joke_score = joke_score -2 WHERE user_id = '{user.id}';")
    
    #possible outcomes
    outcomes = {
        range(1,2):(f"UPDATE user_joker_score SET joke_score = 0 WHERE user_id = '{user.id}';","Return to zero...\n(Score set to 0)"),
        range(2,3):(f"UPDATE user_joker_score SET joke_score = joke_score * -1 WHERE user_id = '{user.id}';","Oh no...\n(Score set negative)"),
        range(3,4):(f"UPDATE user_joker_score SET joke_score = 1 WHERE user_id = '{user.id}';","Points set to 1... you are forever cursed to have an odd score..."),
        range(4,8):(f"UPDATE user_joker_score SET joke_score = joke_score /2 WHERE user_id = '{user.id}';","Points halved..."),
        range(9,11):(f"UPDATE user_joker_score SET joke_score = joke_score * 0.75 WHERE user_id = '{user.id}';","yikes...\n(Points reduced by 25%)"),
        range(11,13):(f"UPDATE user_joker_score SET joke_score = joke_score - 10 WHERE user_id = '{user.id}';","ough,, bad luck...\n(-10)"),
        range(9,30):(f"UPDATE user_joker_score SET joke_score = joke_score + 0  WHERE user_id = '{user.id}';","Nothing happens..."),
        range(30,43):(f"UPDATE user_joker_score SET joke_score = joke_score + 4 WHERE user_id = '{user.id}';","You got your points back plus some more!\n(points back +2)"),
        range(43,46):(f"UPDATE user_joker_score SET joke_score = joke_score + 6 WHERE user_id = '{user.id}';","You got your points back, and then some!\n(points back +4)"),
        range(46,47):(f"UPDATE user_joker_score SET joke_score = joke_score + 12 WHERE user_id = '{user.id}';","wooo thats what its all about baby, dedication!!\n(points back +10)"),
        range(47,48):(f"UPDATE user_joker_score SET joke_score = joke_score * 1.5 WHERE user_id = '{user.id}';","Points increased by 50%!"),
        range(48,49):(f"UPDATE user_joker_score SET joke_score = joke_score * 2 WHERE user_id = '{user.id}';","YOWZA!!!!\n(Points doubled!)"),
        range(49,50):(f"UPDATE user_joker_score SET joke_score = joke_score * 3 WHERE user_id = '{user.id}';","OMGGGGG!!!\n(Points TRIPLED!)"),
        range(50,51):(f"UPDATE user_joker_score SET joke_score = joke_score * 10  WHERE user_id = '{user.id}';","WOAHHH!!!!!!\n(POINTS x10!!!)")
    }
    
    roll, (query, explanation) = roll_outcome(outcomes)
    
    await postgres.write(query)
    await interaction.followup.send(f"🎲🎰Lets go gambling!!!🎰🎲\n{user.mention} Inserts 2 joker coins into the gambling machine...{explanation}")
    return


def roll_outcome(outcomes):
    roll = randint(1,51)
    print(f"rolled a {roll}")
    for range_, outcome in outcomes.items():
        if roll in range_:
            return roll, outcome
    
        
        
    