import discord
from data import postgres
from random import randint
import os

async def gamble_points(interaction: discord.Interaction):
    await interaction.response.defer()
    
    # dm restriction
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send("we are literally in DMs rn bro u cant do that here...")
        return
    
    # read the current score
    user = interaction.user
    score = await postgres.read(f"SELECT joke_score FROM user_joker_score WHERE user_id = '{user.id}';")
    score = score[0][0]
    
    # cant play if ur broke
    if score - 1 < 0:
        await interaction.followup.send(f"{user.mention} lmaooo ur broke sry no gambling for u loser")
        return
    
    # pay a coin for a spin
    await postgres.write(f"UPDATE user_joker_score SET joke_score = joke_score -1 WHERE user_id = '{user.id}';")
    
    # possible outcomes
    outcomes = {
        range(1,3):(f"UPDATE user_joker_score SET joke_score = 0 WHERE user_id = '{user.id}';","Return to zero...\n(Score set to 0)", "return_to_0.gif"),
        range(3,6):(f"UPDATE user_joker_score SET joke_score = joke_score * -1 WHERE user_id = '{user.id}';","Oh no...\n(Score set negative)", "negative.gif"),
        range(6,9):(f"UPDATE user_joker_score SET joke_score = 1 WHERE user_id = '{user.id}';","Points set to 1... you are forever cursed to have an odd score...", "curse.gif"),
        range(9,12):(f"UPDATE user_joker_score SET joke_score = joke_score /2 WHERE user_id = '{user.id}';","Points halved...","-50%.gif"),
        range(12,17):(f"UPDATE user_joker_score SET joke_score = joke_score * 0.75 WHERE user_id = '{user.id}';","yikes...\n(Points reduced by 25%)","-25%.gif"),
        range(17,20):(f"UPDATE user_joker_score SET joke_score = joke_score - 10 WHERE user_id = '{user.id}';","ough,, bad luck...\n(-10)","-10.gif"),
        range(20,30):(f"UPDATE user_joker_score SET joke_score = joke_score + 0  WHERE user_id = '{user.id}';","Nothing happens...", "nothing01.gif"),
        range(30,40):(f"UPDATE user_joker_score SET joke_score = joke_score + 0  WHERE user_id = '{user.id}';","Nothing happens...", "nothing02.gif"),
        range(40,50):(f"UPDATE user_joker_score SET joke_score = joke_score + 0  WHERE user_id = '{user.id}';","Nothing happens...", "nothing03.gif"),
        range(50,60):(f"UPDATE user_joker_score SET joke_score = joke_score + 0  WHERE user_id = '{user.id}';","Nothing happens...", "nothing04.gif"),
        range(60,74):(f"UPDATE user_joker_score SET joke_score = joke_score + 3 WHERE user_id = '{user.id}';","You got your points back plus some more!\n(points back +2)", "+2.gif"),
        range(74,84):(f"UPDATE user_joker_score SET joke_score = joke_score + 5 WHERE user_id = '{user.id}';","You got your points back, and then some!\n(points back +4)","+4.gif"),
        range(84,90):(f"UPDATE user_joker_score SET joke_score = joke_score + 11 WHERE user_id = '{user.id}';","wooo thats what its all about baby, dedication!!\n(points back +10)","+10.gif"),
        range(90,94):(f"UPDATE user_joker_score SET joke_score = joke_score + 21 WHERE user_id = '{user.id}';","20 Points!","score_x1.5.gif"),
        range(94,97):(f"UPDATE user_joker_score SET joke_score = joke_score + 1 * 2 WHERE user_id = '{user.id}';","YOWZA!!!!\n(Points doubled!)", "score_x2.gif"),
        range(97,100):(f"UPDATE user_joker_score SET joke_score = joke_score + 1 * 10 WHERE user_id = '{user.id}';","OMGGGGG!!!\n(Points x10!!!)", "score_x3.gif"),
        range(100,101):(f"UPDATE user_joker_score SET joke_score = joke_score + 1001  WHERE user_id = '{user.id}';","WOAHHH!!!!!!\n(ONE THOUSAND POINTS!!!)", "score_x10.gif")
    }
    
    # get the outcome
    roll, (query, explanation, media) = roll_outcome(outcomes)
    
    # comit the change in the db
    await postgres.write(query)
    
    # find the path to the media folder
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir,'..', '..', '..', 'assets', 'media', 'slots', media)
    
    # send the corresponding gif
    file=discord.File(file_path)
    await interaction.channel.send(file=file)
    await interaction.channel.send(explanation)
    await interaction.followup.send(f"🎲🎰Lets go gambling!!!🎰🎲\n{user.mention} Inserts a joker coin into the gambling machine...")
    return

def roll_outcome(outcomes):
    roll = randint(1,100)
    for range_, outcome in outcomes.items():
        if roll in range_:
            return roll, outcome