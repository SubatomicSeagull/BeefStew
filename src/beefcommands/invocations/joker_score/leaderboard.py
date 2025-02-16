import discord
from data import postgres

async def retrive_top_scores(interaction: discord.Interaction, bot):
    await interaction.response.defer()
    # read the top 10 scores from the db
    rows = await postgres.read("SELECT user_id, joke_score FROM user_joker_score ORDER BY joke_score DESC LIMIT 10")
    
    # embed header
    leaderboard = discord.Embed(title= "Joke Score Leaderboard", color=discord.Color.gold())
    leaderboard.set_author(name="Beefstew", icon_url=bot.user.avatar.url)

    # read the rows returned from the sql query and add them to the embed body
    if not rows:
        leaderboard.description = "wha? no scores??"
    else:
        leaderboard_content = ""
        for rank, row in enumerate(rows, start=1):
            leaderboard_content += f"**{rank}.** <@{row[0]}> - `{row[1]}` points\n"
        leaderboard.description = leaderboard_content
    await interaction.followup.send(embed=leaderboard)
    
async def retrive_low_scores(interaction: discord.Interaction, bot):
    await interaction.response.defer()
    # read the lowest 10 scores from the db
    rows = await postgres.read("SELECT user_id, joke_score FROM user_joker_score ORDER BY joke_score ASC LIMIT 10")
    
    # embed header
    leaderboard = discord.Embed(title= "# Joke Score Loserboard", color=discord.Color.fuchsia())
    leaderboard.set_author(name="Beefstew", icon_url=bot.user.avatar.url)

    # read the rows returned from the sql query and add them to the embed body
    if not rows:
        leaderboard.description = "wha? no scores??"
    else:
        leaderboard_content = ""
        for rank, row in enumerate(rows, start=1):
            leaderboard_content += f"**{rank}.** <@{row[0]}> - `{row[1]}` points\n"
        leaderboard.description = leaderboard_content
    await interaction.followup.send(embed=leaderboard)