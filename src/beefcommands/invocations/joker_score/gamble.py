import discord
from beefutilities import TTS
from data import postgres
from random import randint
from beefutilities.IO import file_io
from beefcommands.invocations.joker_score.read_joker_score import retrieve_joke_score
from beefcommands.invocations.joker_score.change_joker_score import set_highest_score, set_lowest_score, add_score_change_record, change_joke_score

async def gamble_points(interaction: discord.Interaction):
    await interaction.response.defer()

    # dm restriction
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send("we are literally in DMs rn bro u cant do that here...")
        return

    # read the current score
    user = interaction.user
    score = await retrieve_joke_score(user)

    # cant play if ur broke
    if score - 1 < 0:
        await interaction.followup.send(f"{user.mention} lmaooo ur broke sry no gambling for u loser")
        await TTS.speak_output(interaction, "lmaooo ur broke sry no gambling for u loser")
        return
    
    current_score = await postgres.read(f"SELECT current_score FROM joke_scores WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';")
    current_score = current_score[0][0]

    outcomes = {
        range(1,3):((current_score*-1),"Return to zero...\n(Score set to 0)", "return_to_0.gif"),
        range(3,6):(((current_score*2)*-1),"Oh no...\n(Score set negative)", "negative.gif"),
        range(6,9):(((current_score*-1)+1),"Points set to 1... you are forever cursed to have an odd score...", "curse.gif"),
        range(9,12):(((current_score/2)*-1),"Points halved...","-50%.gif"),
        range(12,17):(((current_score/4)*-1),"yikes...\n(Points reduced by 25%)","-25%.gif"),
        range(17,20):(-10,"ough,, bad luck...\n(-10)","-10.gif"),
        range(20,30):(0,"Nothing happens...", "nothing01.gif"),
        range(30,40):(0,"Nothing happens...", "nothing02.gif"),
        range(40,50):(0,"Nothing happens...", "nothing03.gif"),
        range(50,60):(0,"Nothing happens...", "nothing04.gif"),
        range(60,74):(3,"You got your points back plus some more!\n(points back +2)", "+2.gif"),
        range(74,84):(5,"You got your points back, and then some!\n(points back +4)","+4.gif"),
        range(84,90):(11,"wooo thats what its all about baby, dedication!!\n(points back +10)","+10.gif"),
        range(90,94):(20,"20 Points!","score_x1.5.gif"),
        range(94,97):((current_score*2),"YOWZA!!!!\n(Points doubled!)", "score_x2.gif"),
        range(97,100):((current_score*10),"OMGGGGG!!!\n(Points x10!!!)", "score_x3.gif"),
        range(100,101):(1001,"WOAHHH!!!!!!\n(ONE THOUSAND POINTS!!!)", "score_x10.gif")
    }

    roll, (value, explanation, media) = roll_outcome(outcomes)

    # change the users score by adding the value of the gambling outcome minus the 1 point to play
    await change_joke_score(user, user, value-1, "gambling")

    # find the path to the media folder
    file_path = file_io.construct_media_path(f"slots/{media}")

    # send the corresponding gif
    file=discord.File(file_path)
    await interaction.channel.send(file=file)
    await interaction.channel.send(explanation)
    await interaction.followup.send(f"🎲🎰Lets go gambling!!!🎰🎲\n{user.mention} inserts a joker coin into the gambling machine...")
    if user.nick:
        await TTS.speak_output(interaction, f"Lets go gambling!\n {user.nick} inserts a joker coin into the gambling machine...")
    else:
        await TTS.speak_output(interaction, f"Lets go gambling!\n {user.name} inserts a joker coin into the gambling machine...")
    
    return

def roll_outcome(outcomes):
    roll = randint(1,100)
    for range_, outcome in outcomes.items():
        if roll in range_:
            return roll, outcome