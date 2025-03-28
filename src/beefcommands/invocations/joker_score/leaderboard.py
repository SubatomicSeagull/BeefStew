import discord
from data import postgres

async def retrive_top_scores(interaction: discord.Interaction, bot):
    await interaction.response.defer()
    # read the top 10 scores from the db
    rows = await postgres.read(f"SELECT user_id, current_score FROM joke_scores WHERE guild_id = '{interaction.guild.id}' ORDER BY current_score DESC LIMIT 10;")
    highest = await postgres.read(f"SELECT user_id, highest_score FROM joke_scores WHERE guild_id = '{interaction.guild.id}' ORDER BY highest_score DESC LIMIT 1;")
    
    # embed header
    leaderboard = discord.Embed(title= "Joke Score Leaderboard", color=discord.Color.gold())
    leaderboard.set_author(name="Beefstew", icon_url=bot.user.avatar.url)

    # read the rows returned from the sql query and add them to the embed body
    if not rows:
        leaderboard.description = "wha? no scores??"
    else:
        leaderboard_content = ""
        leaderboard_content += f"**Top Joker of All Time:** <@{highest[0][0]}>: `{highest[0][1]}` points\n\n"
        for rank, row in enumerate(rows, start=1):
            if row[0] == 99:
                leaderboard_content += f"**{rank}.** Hawk Tuah Jar: `{row[1]}` points\n"
            else:
                leaderboard_content += f"**{rank}.** <@{row[0]}>: `{row[1]}` points\n"
        leaderboard.description = leaderboard_content
    await interaction.followup.send(embed=leaderboard)
    
async def retrive_low_scores(interaction: discord.Interaction, bot):
    await interaction.response.defer()
    # read the lowest 10 scores from the db
    rows = await postgres.read(f"SELECT user_id, current_score FROM joke_scores WHERE guild_id = '{interaction.guild.id}' ORDER BY current_score ASC LIMIT 10;")
    lowest = await postgres.read(f"SELECT user_id, lowest_score FROM joke_scores WHERE guild_id = '{interaction.guild.id}' ORDER BY lowest_score ASC LIMIT 1;")

    
    # embed header
    leaderboard = discord.Embed(title= "Joke Score Loserboard", color=discord.Color.fuchsia())
    leaderboard.set_author(name="Beefstew", icon_url=bot.user.avatar.url)

    # read the rows returned from the sql query and add them to the embed body
    if not rows:
        leaderboard.description = "wha? no scores??"
    else:
        leaderboard_content = ""
        leaderboard_content += f"**Least funny ever:** <@{lowest[0][0]}>: `{lowest[0][1]}` points\n\n"
        for rank, row in enumerate(rows, start=1):
            if row[0] == 99:
                leaderboard_content += f"**{rank}.** Hawk Tuah Jar: `{row[1]}` points\n"
            else:
                leaderboard_content += f"**{rank}.** <@{row[0]}>: `{row[1]}` points\n"
        leaderboard.description = leaderboard_content
    await interaction.followup.send(embed=leaderboard)