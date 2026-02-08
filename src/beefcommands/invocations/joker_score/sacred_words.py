from random import randrange
import os
from collections import deque
from itertools import islice
import datetime
from beefutilities.IO import file_io
from beefcommands.invocations.joker_score import swear_jar
from beefcommands.invocations.joker_score.change_joker_score import change_joke_score
from beefcommands.invocations.joker_score.read_joker_score import retrieve_joke_score
from data import postgres
import discord

"""
get two words, one of them is the saint word, and one of them is the sinner word for that day
the saint word gets the payout from the swear jar, 
the sinner word gets half their points put into the jar.
"""

g_saint_word = ""
g_sinner_word = ""

def load_sacred_words():
    global g_saint_word
    global g_sinner_word
    
    g_saint_word = get_random_word().strip()
    
    g_sinner_word = get_random_word().strip()
    
    print(f"The saint word for {datetime.datetime.now().strftime("%d/%m/%Y")} is {g_saint_word}")
    print(f"The sinner word for {datetime.datetime.now().strftime("%d/%m/%Y")} is {g_sinner_word}")
    
    
async def check_sacred_word(message: discord.Message):
    global g_saint_word
    global g_sinner_word
    
    if g_sinner_word != "" or g_saint_word != "":
        if g_sinner_word.lower() in message.content.lower():
            await sinner_word_curse(message.author, message)
            return
        elif g_saint_word.lower() in message.content.lower():
            await saint_word_blessing(message.author, message)
            return
        else:
            return
    return

def get_random_word():
    with open(file_io.construct_assets_path("dictionary.txt"), "r") as f:
        # count the number of lines
        n = sum(1 for _ in f)
        
        # get a random line number
        i = randrange(n)
        
        # reset the file stream position to the start
        f.seek(0)
        deque(islice(f, i - 1), maxlen=0)
        
        # then we just return the next line
        return next(f)

def clear_sacred_words():
    global g_saint_word
    g_saint_word = ""
    global g_sinner_word
    g_sinner_word = ""
    
    
async def saint_word_blessing(victim: discord.Member, message: discord.Message):
    global g_saint_word
    print(f"{victim} said the saint word!")
    await message.reply(content=f"{victim.mention} said the saint word **{g_saint_word}**! \nBlessing them with the swear jar payout!!!", file=discord.File(await swear_jar.generate_payout_gif([victim]), filename="payout.gif"))
    await swear_jar.swear_jar_payout([victim])
    load_sacred_words()
    

async def sinner_word_curse(victim: discord.Member, message: discord.Message):
    global g_sinner_word
    print(f"{victim} said the sinner word!")
    await message.reply(content=f"{victim.mention} said the sinner word **{g_sinner_word}**! \nCursing them by taking half their points and putting it in the swear jar!!!", file=discord.File(file_io.construct_media_path("sinner_jar.gif"), filename="swearjar.gif"))
    score = await retrieve_joke_score(victim)
    value = score//2
    await change_joke_score(await victim.guild.fetch_member(os.getenv("CLIENTID")), victim, -value, "sinner word curse")
    await postgres.write(f"UPDATE public.joke_scores SET current_score = current_score + {value} WHERE user_id = '99' AND guild_id = '{message.guild.id}';")
    load_sacred_words()