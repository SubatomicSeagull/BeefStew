import discord
from data import postgres
from beefcommands.invocations.joker_score.joker_registration import is_registered, register_user

async def retrieve_joke_score(user: discord.Member):
    if not await is_registered(user):
        await register_user(user)
    joke_score = await (postgres.read(f"SELECT current_score FROM joke_scores WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';"))
    score = joke_score[0][0]
    return int(score)

async def get_user_highest_score(user: discord.Member):
    if not await is_registered(user):
        await register_user(user)
    highest_score = await (postgres.read(f"SELECT highest_score FROM joke_scores WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';"))
    score = highest_score[0][0]
    return int(score)

async def get_user_lowest_score(user: discord.Member):
    if not await is_registered(user):
        await register_user(user)
    lowest_score = await (postgres.read(f"SELECT lowest_score FROM joke_scores WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';"))
    score = lowest_score[0][0]
    return int(score)

# probably not going to use this
async def get_multiplier(user: discord.Member):
    winner = discord.utils.get(user.guild.roles, name = "the funniest person ever")
    loser = discord.utils.get(user.guild.roles, name = "tonights biggest loser")
    if winner in user.roles:
        return 1.5
    elif loser in user.roles:
        return 0
    else:
        return 1

async def score(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer()

    # dm restriction
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send("we are literally in DMs rn bro u cant do that here...")
        return

    # check to see if the user is registered in the db, if not, register them
    if not await is_registered(user):
        await register_user(user)
    try:
        score = await retrieve_joke_score(user)
        await interaction.followup.send(f"{user.mention}'s joker score: **{score}**!")
    except Exception as e:
        postgres.log_error(e)
        await interaction.followup.send(f"couldnt find {user.name}'s score :( ({e}))")