import json
import discord
from beefcommands.invocations.joker_score.change_joker_score import change_joke_score
from data import postgres
from beefutilities.IO import file_io

def load_swears():
    swears = []
    file_path = file_io.construct_assets_path('responses.json')
    with open(file_path, "r") as file:
        swears = json.load(file)["swears"]
    return swears


async def swear_jar_penalty(victim: discord.Member):
    # take 2 points from the victim and give it to the jar
    await change_joke_score(victim, victim, -2, "swear jar penalty")
    await postgres.write(f"UPDATE public.joke_scores SET current_score = current_score + 2 WHERE user_id = '99' AND guild_id = '{victim.guild.id}';")

async def get_swear_jar_score(guild: discord.Guild):
    joke_score = await (postgres.read(f"SELECT current_score FROM public.joke_scores WHERE user_id = '99' AND guild_id = '{guild.id}';"))
    score = joke_score[0][0]
    return score

async def swear_jar_payout(victims):
    # take the point from the jar and distribute them to the victims
    pass