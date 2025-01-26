import discord
from data import postgres
from random import randint
import os

async def gamble_points(interaction: discord.Interaction):
    await interaction.response.defer()
    user = interaction.user
    score = await postgres.read(f"SELECT joke_score FROM user_joker_score WHERE user_id = '{user.id}';")
    score = score[0][0]
    
    if score - 2 < 0:
        await interaction.followup.send(f"{user.mention} lmaooo ur broke sry no gambling for u loser")
        return
        
    await postgres.write(f"UPDATE user_joker_score SET joke_score = joke_score -2 WHERE user_id = '{user.id}';")
    
    #possible outcomes
    outcomes = {
        range(1,2):(f"UPDATE user_joker_score SET joke_score = 0 WHERE user_id = '{user.id}';","Return to zero...\n(Score set to 0)", "return_to_0.gif"),
        range(2,3):(f"UPDATE user_joker_score SET joke_score = joke_score * -1 WHERE user_id = '{user.id}';","Oh no...\n(Score set negative)", "negative.gif"),
        range(3,4):(f"UPDATE user_joker_score SET joke_score = 1 WHERE user_id = '{user.id}';","Points set to 1... you are forever cursed to have an odd score...", "curse.gif"),
        range(4,8):(f"UPDATE user_joker_score SET joke_score = joke_score /2 WHERE user_id = '{user.id}';","Points halved...","-50%.gif"),
        range(8,11):(f"UPDATE user_joker_score SET joke_score = joke_score * 0.75 WHERE user_id = '{user.id}';","yikes...\n(Points reduced by 25%)","-25%.gif"),
        range(11,13):(f"UPDATE user_joker_score SET joke_score = joke_score - 10 WHERE user_id = '{user.id}';","ough,, bad luck...\n(-10)","-10.gif"),
        range(13,15):(f"UPDATE user_joker_score SET joke_score = joke_score + 0  WHERE user_id = '{user.id}';","Nothing happens...", "nothing01.gif"),
        range(15,20):(f"UPDATE user_joker_score SET joke_score = joke_score + 0  WHERE user_id = '{user.id}';","Nothing happens...", "nothing02.gif"),
        range(20,25):(f"UPDATE user_joker_score SET joke_score = joke_score + 0  WHERE user_id = '{user.id}';","Nothing happens...", "nothing03.gif"),
        range(25,30):(f"UPDATE user_joker_score SET joke_score = joke_score + 0  WHERE user_id = '{user.id}';","Nothing happens...", "nothing04.gif"),
        range(30,43):(f"UPDATE user_joker_score SET joke_score = joke_score + 4 WHERE user_id = '{user.id}';","You got your points back plus some more!\n(points back +2)", "+2.gif"),
        range(43,46):(f"UPDATE user_joker_score SET joke_score = joke_score + 6 WHERE user_id = '{user.id}';","You got your points back, and then some!\n(points back +4)","+4.gif"),
        range(46,47):(f"UPDATE user_joker_score SET joke_score = joke_score + 12 WHERE user_id = '{user.id}';","wooo thats what its all about baby, dedication!!\n(points back +10)","+10.gif"),
        range(47,48):(f"UPDATE user_joker_score SET joke_score = joke_score * 1.5 WHERE user_id = '{user.id}';","Points increased by 50%!","score_x1.5.gif"),
        range(48,49):(f"UPDATE user_joker_score SET joke_score = joke_score * 2 WHERE user_id = '{user.id}';","YOWZA!!!!\n(Points doubled!)", "score_x2.gif"),
        range(49,50):(f"UPDATE user_joker_score SET joke_score = joke_score * 3 WHERE user_id = '{user.id}';","OMGGGGG!!!\n(Points TRIPLED!)", "score_x3.gif"),
        range(50,51):(f"UPDATE user_joker_score SET joke_score = joke_score * 10  WHERE user_id = '{user.id}';","WOAHHH!!!!!!\n(POINTS x10!!!)", "score_x10.gif")
    }
    

    roll, (query, explanation, media) = roll_outcome(outcomes)
    
    await postgres.write(query)
    
    current_dir = os.path.dirname(__file__)
    print(current_dir)
    file_path = os.path.join(current_dir,'..', '..', '..', 'assets', 'media', 'slots', media)
    print(file_path)
    file=discord.File(file_path)
    await interaction.channel.send(file=file)
    await interaction.channel.send(explanation)
    await interaction.followup.send(f"🎲🎰Lets go gambling!!!🎰🎲\n{user.mention} Inserts 2 joker coins into the gambling machine...")
    return

def roll_outcome(outcomes):
    roll = randint(1,50)
    print(f"rolled a {roll}")
    for range_, outcome in outcomes.items():
        if roll in range_:
            return roll, outcome