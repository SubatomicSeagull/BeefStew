import discord
from beefutilities import TTS
from data import postgres

async def retrieve_top_scores(interaction: discord.Interaction, bot):
    await interaction.response.defer()
    # read all scores from the db, we'll limit in Python
    rows = await postgres.read(f"SELECT user_id, current_score, user_name, user_display_name FROM joke_scores WHERE guild_id = '{interaction.guild.id}' ORDER BY current_score DESC;")
    highest = await postgres.read(f"SELECT user_id, highest_score, user_name, user_display_name FROM joke_scores WHERE user_id != '99' AND guild_id = '{interaction.guild.id}' ORDER BY highest_score DESC LIMIT 1;")
    tuahjar = await postgres.read(f"SELECT current_score FROM joke_scores WHERE guild_id = '{interaction.guild.id}' AND user_id = '99';")

    leaderboard = discord.Embed(title = "Joke Score Leaderboard", color = discord.Color.gold())
    leaderboard.set_author(name = "Beefstew", icon_url = bot.user.avatar.url)
    # read the rows returned from the sql query and add them to the embed body
    if not rows:
        leaderboard.description = "wha? no scores??"
    else:
        speech_content = "Joke score leaderboard. \n"
        leaderboard_content = ""
        leaderboard_content += f"**Top Joker of All Time:** <@{highest[0][0]}>: `{highest[0][1]}` points\n\n"
        rank = 1
        for row in rows:
            if row[0] == 99:
                continue
            if rank > 10:
                break
            leaderboard_content += f"**{rank}.** <@{row[0]}>: `{row[1]}` points\n"
            if row[3] == None or row[3] == "None":
                speech_content += f"Number {rank} is {row[2]} with {row[1]} points. \n"
            else:
                speech_content += f"Number {rank} is {row[3]} with {row[1]} points. \n"
            rank += 1
        leaderboard_content += f"\n\n**Hawk Tuah Jar:** `{tuahjar[0][0]}` points"
        speech_content += f"The Hawk Tuah Jar has {tuahjar[0][0]} points. \n"
        if highest[0][3] == None or highest[0][3] == "None":
            speech_content += f"and the top joker of all time is {highest[0][2]} with {highest[0][1]}` points."
        else:
            speech_content += f"and the top joker of all time is {highest[0][3]} with {highest[0][1]}` points."
            
        leaderboard.description = leaderboard_content
    await interaction.followup.send(embed=leaderboard)
    await TTS.speak_output(interaction, speech_content)
    
async def retrieve_low_scores(interaction: discord.Interaction, bot):
    await interaction.response.defer()
    # read all scores from the db, we'll limit in Python
    rows = await postgres.read(f"SELECT user_id, current_score, user_name, user_display_name FROM joke_scores WHERE guild_id = '{interaction.guild.id}' ORDER BY current_score ASC;")
    lowest = await postgres.read(f"SELECT user_id, lowest_score, user_name, user_display_name FROM joke_scores WHERE user_id != '99' AND guild_id = '{interaction.guild.id}' ORDER BY lowest_score ASC LIMIT 1;")

    # embed header
    leaderboard = discord.Embed(title = "Joke Score Loserboard", color = discord.Color.fuchsia())
    leaderboard.set_author(name = "Beefstew", icon_url = bot.user.avatar.url)

    # read the rows returned from the sql query and add them to the embed body
    if not rows:
        leaderboard.description = "wha? no scores??"
    else:
        speech_content = "Joke score loserboard.\n "
        leaderboard_content = ""
        leaderboard_content += f"**Least funny ever:** <@{lowest[0][0]}>: `{lowest[0][1]}` points\n\n"
        rank = 1
        for row in rows:
            if row[0] == 99:
                continue
            if rank > 10:
                break
            leaderboard_content += f"**{rank}.** <@{row[0]}>: `{row[1]}` points\n"
            if row[3] == None or row[3] == "None":
                speech_content += f"Number {rank} is {row[2]} with {row[1]} points. \n"
            else:
                speech_content += f"Number {rank} is {row[3]} with {row[1]} points. \n"
            rank += 1
        if lowest[0][3] == None or lowest[0][3] == "None":
            speech_content += f"and the least funny person ever is {lowest[0][2]} with {lowest[0][1]} points."
        else:
            speech_content += f"and the least funny person ever is {lowest[0][3]} with {lowest[0][1]}points."
            
        leaderboard.description = leaderboard_content
    await interaction.followup.send(embed = leaderboard)
    await TTS.speak_output(interaction, speech_content)
