import discord
from data import postgres
from beefutilities.json_handling import load_element
import random
from beefcommands.invocations.joker_score.read_joker_score import get_multilplier
from beefcommands.invocations.joker_score.joker_registration import is_registered, register_user


async def change_joke_score(self: discord.Member, user: discord.Member, value):
    # check to see of a user is registerd in the db, if not, register them
    if not await is_registered(user):
        await register_user(user)
    
    # cant +2 yourself
    if self.id == user.id and value > 0:
        return "cant do that lol lmao loser"
    
    # but you can -2 yourself
    elif self.id == user.id and value < 0:      
        await postgres.write(f"UPDATE user_joker_score SET joke_score = joke_score + {value} WHERE user_id = '{user.id}';")
        await postgres.write(f"UPDATE user_joker_score SET member_name = '{user.nick}' WHERE user_id = '{user.id}';")
        return f"{self.mention} -2'd themselves for some reason... oh well!\n {await get_joke_response_negative(user)}"
    
    
    try:
        # get the multiplier (this will always be 1 coz i dont think we are going to use this mechanic anymore)
        mult = await get_multilplier(user)
        score = value * mult
        await postgres.write(f"UPDATE user_joker_score SET joke_score = joke_score + {score} WHERE user_id = '{user.id}';")
        await postgres.write(f"UPDATE user_joker_score SET member_name = '{user.nick}' WHERE user_id = '{user.id}';")
        
        # send positive or negative message based on the value
        if score > 0: 
            return (await get_joke_response_positive(user))
        else:
            return (await get_joke_response_negative(user))
    
    except Exception as e:
        await postgres.log_error(e)
        return (f"couldnt change score for {user.name} :( ({e}))")

async def clear_joke_score(user: discord.Member):
    await postgres.write(f"UPDATE user_joker_score SET joke_score = 0 WHERE user_id = '{user.id}';")
    
async def get_joke_response_positive(member: discord.Member):
    # define the tag to reformat the response from responses.json so that it mentions the yser    
    jokertag = type('Joker', (object,), {"mention": member.mention})()
    responses = load_element("responses.json", "joke_responses_positive")
    
    # return a random response from the json file
    chosen_response = random.choice(responses)
    chosen_response = chosen_response.format(joker=jokertag)
    return chosen_response

async def get_joke_response_negative( member: discord.Member):
    # define the tag to reformat the response from responses.json so that it mentions the yser 
    jokertag = type('Joker', (object,), {"mention": member.mention})()
    responses = load_element("responses.json", "joke_responses_negative")
    
    # return a random response from the json file   
    chosen_response = random.choice(responses)
    chosen_response = chosen_response.format(joker=jokertag)
    return chosen_response

async def plus2(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.defer()
    
    # dm restriction
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send("we are literally in DMs rn bro u cant do that here...")
        return
    
    await interaction.followup.send(await change_joke_score(interaction.user, member, 2))

async def minus2(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.defer()
    
    # dm restriction
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send("we are literally in DMs rn bro u cant do that here...")
        return
    
    await interaction.followup.send(await change_joke_score(interaction.user, member, -2))