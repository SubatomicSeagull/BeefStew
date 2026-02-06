from random import randrange
from collections import deque
from itertools import islice
import datetime
from beefutilities.IO import file_io
from beefcommands.invocations.joker_score.swear_jar import swear_jar_payout
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
    
    if g_saint_word == "":
        g_saint_word = get_random_word().strip()
    
    if g_sinner_word == "":
        g_sinner_word = get_random_word().strip()
    print(f"The saint word for {datetime.datetime.now().strftime("%d/%m/%Y")} is {g_saint_word}")
    print(f"The sinner word for {datetime.datetime.now().strftime("%d/%m/%Y")} is {g_sinner_word}")

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
    
    
async def saint_word_blessing(victim: discord.Member):
    #the user will get all the points in the swear jar
    
    pass

async def sinner_word_curse():
    #the user will have half their points taken away and put into the swear jar
    pass