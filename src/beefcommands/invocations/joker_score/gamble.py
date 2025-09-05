import discord
from beefutilities.TTS import speak
from data import postgres
from random import randint
from beefutilities.IO import file_io
from beefcommands.invocations.joker_score.read_joker_score import retrieve_joke_score
from beefcommands.invocations.joker_score.change_joker_score import set_highest_score, set_lowest_score

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
        await speak.speak_output(interaction, "lmaooo ur broke sry no gambling for u loser")
        return

    # pay a coin for a spin
    await postgres.write(f"UPDATE public.joke_scores SET current_score = current_score -1 WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';")

    # possible outcomes
    outcomes = {
        range(1,3):(f"UPDATE public.joke_scores SET current_score = 0 WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';","Return to zero...\n(Score set to 0)", "return_to_0.gif"),
        range(3,6):(f"UPDATE public.joke_scores SET current_score = current_score * -1 WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';","Oh no...\n(Score set negative)", "negative.gif"),
        range(6,9):(f"UPDATE public.joke_scores SET current_score = 1 WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';","Points set to 1... you are forever cursed to have an odd score...", "curse.gif"),
        range(9,12):(f"UPDATE public.joke_scores SET current_score = current_score /2 WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';","Points halved...","-50%.gif"),
        range(12,17):(f"UPDATE public.joke_scores SET current_score = current_score * 0.75 WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';","yikes...\n(Points reduced by 25%)","-25%.gif"),
        range(17,20):(f"UPDATE public.joke_scores SET current_score = current_score - 10 WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';","ough,, bad luck...\n(-10)","-10.gif"),
        range(20,30):(f"UPDATE public.joke_scores SET current_score = current_score + 0  WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';","Nothing happens...", "nothing01.gif"),
        range(30,40):(f"UPDATE public.joke_scores SET current_score = current_score + 0  WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';","Nothing happens...", "nothing02.gif"),
        range(40,50):(f"UPDATE public.joke_scores SET current_score = current_score + 0  WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';","Nothing happens...", "nothing03.gif"),
        range(50,60):(f"UPDATE public.joke_scores SET current_score = current_score + 0  WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';","Nothing happens...", "nothing04.gif"),
        range(60,74):(f"UPDATE public.joke_scores SET current_score = current_score + 3 WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';","You got your points back plus some more!\n(points back +2)", "+2.gif"),
        range(74,84):(f"UPDATE public.joke_scores SET current_score = current_score + 5 WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';","You got your points back, and then some!\n(points back +4)","+4.gif"),
        range(84,90):(f"UPDATE public.joke_scores SET current_score = current_score + 11 WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';","wooo thats what its all about baby, dedication!!\n(points back +10)","+10.gif"),
        range(90,94):(f"UPDATE public.joke_scores SET current_score = current_score + 21 WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';","20 Points!","score_x1.5.gif"),
        range(94,97):(f"UPDATE public.joke_scores SET current_score = current_score + 1 * 2 WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';","YOWZA!!!!\n(Points doubled!)", "score_x2.gif"),
        range(97,100):(f"UPDATE public.joke_scores SET current_score = current_score + 1 * 10 WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';","OMGGGGG!!!\n(Points x10!!!)", "score_x3.gif"),
        range(100,101):(f"UPDATE public.joke_scores SET current_score = current_score + 1001  WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';","WOAHHH!!!!!!\n(ONE THOUSAND POINTS!!!)", "score_x10.gif")
    }

    # get the outcome
    roll, (query, explanation, media) = roll_outcome(outcomes)

    # commit the change in the db
    await postgres.write(query)

    # update highest and lowest scores
    await set_highest_score(user, await retrieve_joke_score(user))
    await set_lowest_score(user, await retrieve_joke_score(user))

    # find the path to the media folder
    file_path = file_io.construct_media_path(f"slots/{media}")

    # send the corresponding gif
    file=discord.File(file_path)
    await interaction.channel.send(file=file)
    await interaction.channel.send(explanation)
    await interaction.followup.send(f"🎲🎰Lets go gambling!!!🎰🎲\n{user.mention} Inserts a joker coin into the gambling machine...")
    await speak.speak_output(interaction, f"Lets go gambling! {user.mention} Inserts a joker coin into the gambling machine...")
    return

def roll_outcome(outcomes):
    roll = randint(1,100)
    for range_, outcome in outcomes.items():
        if roll in range_:
            return roll, outcome