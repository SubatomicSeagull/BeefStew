import os
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
        range(1, 11):     ((current_score * -1), "Return to zero...\n(Score set to 0)", "return_to_0.gif"),
        range(11, 18):    (((current_score * 2) * -1), "Oh no...\n(Score set negative)", "negative.gif"),
        range(18, 28):    (((current_score * -1) + 2), "Points set to 1...", "curse.gif"),
        range(28, 58):    (((current_score / 2) * -1), "Points halved...", "-50%.gif"),
        range(58, 98):    (((current_score / 4) * -1), "Points reduced by 25%", "-25%.gif"),
        range(98, 153):   (-10, "ough, bad luck...\n(-10)", "-10.gif"),
        range(153, 743):  (0, "Nothing happens...", "nothing.gif"),
        range(743, 843):  (3, "You got your points back plus some more!\n(+2)", "+2.gif"),
        range(843, 923):  (5, "You got your points back, and then some!\n(+4)", "+4.gif"),
        range(923, 963):  (11, "wooo dedication!!\n(+10)", "+10.gif"),
        range(963, 983):  (20, "20 Points!", "score_x1.5.gif"),
        range(983, 993):  ((current_score + 1), "Points doubled!", "score_x2.gif"),
        range(993, 998):  ((current_score * 10), "Points x10!!!", "score_x3.gif"),
        range(998, 1001): (1001, "ONE THOUSAND POINTS!!!", "score_x10.gif"),
    }

    roll, (value, explanation, media) = roll_outcome(outcomes)

    # change the users score by adding the value of the gambling outcome minus the 1 point to play
    await change_joke_score(await interaction.guild.fetch_member(os.getenv("CLIENTID")), user, value-1, f"gambling: {explanation}")

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
    roll = randint(1,1000)
    for range_, outcome in outcomes.items():
        if roll in range_:
            return roll, outcome