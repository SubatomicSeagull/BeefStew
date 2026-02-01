import discord
from data import postgres
from beefutilities.IO.json_handling import load_element
import random
from beefcommands.invocations.joker_score.read_joker_score import get_multiplier, retrieve_joke_score, get_user_highest_score, get_user_lowest_score
from beefcommands.invocations.joker_score.joker_registration import is_registered_users, is_registered_score, register_user, register_score


async def change_joke_score(scorer: discord.Member, victim: discord.Member, value, reason="NULL"):
    # register the user in the db if theyre not already
    if not await is_registered_users(victim):
        await register_user(victim)
        
    if not await is_registered_score(victim):
        await register_score(victim)

    # cant +2 yourself
    if scorer.id == victim.id and value > 0:
        return "cant do that lol lmao loser"

    try:
        # update the score
        await postgres.write(f"UPDATE public.joke_scores SET current_score = current_score + {value} WHERE user_id = '{victim.id}' AND guild_id = '{victim.guild.id}';")
        
        # update the display name
        await postgres.write(f"UPDATE public.joke_scores SET user_display_name = '{victim.nick}' WHERE user_id = '{victim.id}' AND guild_id = '{victim.guild.id}';")
        
        # add a record of the change in score
        await add_score_change_record(scorer, victim, value, reason)

        # update highest and lowest scores
        current_score = await retrieve_joke_score(victim)
        await set_highest_score(victim, current_score)
        await set_lowest_score(victim, current_score)

        if value > 0:
            print(f"> \033[32m{scorer.name} +{value}'d {victim.name}\033[0m")
            return (await get_joke_response_positive(victim))
        
        elif scorer.id == victim.id and value < 0:
            return f"{scorer.mention} -2'd themselves for some reason... oh well!\n {await get_joke_response_negative(victim)}"
        else:
            print(f"> \033[32m{scorer.name} -2'd {victim.name}\033[0m")
            return (await get_joke_response_negative(victim))
        
    except Exception as e:
        print(f"> \033[31mError while changing the joker score for {victim.name}: {e}\033[0m")
        return (f"couldnt change score for {victim.name} :( ({e}))")

async def clear_joke_score(user: discord.Member):
    await postgres.write(f"UPDATE public.joke_scores SET current_score = 0 WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';")

async def get_joke_response_positive(member: discord.Member):
    jokertag = type('Joker', (object,), {"mention": member.mention})()
    responses = load_element("responses.json", "joke_responses_positive")

    chosen_response = random.choice(responses)
    chosen_response = chosen_response.format(joker = jokertag)
    return chosen_response

async def get_joke_response_negative( member: discord.Member):
    jokertag = type('Joker', (object,), {"mention": member.mention})()
    responses = load_element("responses.json", "joke_responses_negative")

    chosen_response = random.choice(responses)
    chosen_response = chosen_response.format(joker = jokertag)
    return chosen_response

async def plus2(interaction: discord.Interaction, member: discord.Member, reason="NULL"):
    await interaction.response.defer()
    # dm restriction
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send("we are literally in DMs rn bro u cant do that here...")
        return

    await interaction.followup.send(await change_joke_score(interaction.user, member, 2, reason))

async def minus2(interaction: discord.Interaction, member: discord.Member, reason="NULL"):
    await interaction.response.defer()
    # dm restriction
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send("we are literally in DMs rn bro u cant do that here...")
        return

    await interaction.followup.send(await change_joke_score(interaction.user, member, -2, reason))

async def hawk_tuah_penalty(victim: discord.Member):
    # register the user in the db if theyre not already
    if not await is_registered_users(victim):
        await register_user(victim)
        
    if not await is_registered_score(victim):
        await register_score(victim)

    # take 2 points from the victim and update lowest score
    await postgres.write(f"UPDATE public.joke_scores SET current_score = current_score - 2 WHERE user_id = '{victim.id}' AND guild_id = '{victim.guild.id}';")
    await set_lowest_score(victim, await retrieve_joke_score(victim))

    # give 2 points to the jar
    await postgres.write(f"UPDATE public.joke_scores SET current_score = current_score + 2 WHERE user_id = '99' AND guild_id = '{victim.guild.id}';")
    await postgres.write(f"UPDATE public.joke_scores SET user_display_name = '{victim.nick}' WHERE user_id = '{victim.id}' AND guild_id = '{victim.guild.id}';")

    joke_score = await (postgres.read(f"SELECT current_score FROM public.joke_scores WHERE user_id = '99' AND guild_id = '{victim.guild.id}';"))
    score = joke_score[0][0]
    return score

async def set_highest_score(user: discord.Member , score):
    if score > await get_user_highest_score(user):
        await postgres.write(f"UPDATE public.joke_scores SET highest_score = {score} WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';")
    return

async def set_lowest_score(user: discord.Member, score):
    if score < await get_user_lowest_score(user):
        await postgres.write(f"UPDATE public.joke_scores SET lowest_score = {score} WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';")
    return
        
async def add_score_change_record(scorer, victim, value, reason):
    # add a record of the score change inclyuding the before and after, as well as the score change value and a reason if there is any
    current = await postgres.read(f"SELECT id, current_score FROM public.joke_scores WHERE user_id = '{victim.id}' AND guild_id = '{victim.guild.id}';")
    await postgres.write(f"INSERT INTO public.joke_scores_history (joke_score_id, sender_id, score_before, score_after, delta, reason, date) VALUES ({current[0][0]}, {scorer.id}, {current[0][1]-value}, {current[0][1]}, {value}, '{reason}', NOW());")
    return