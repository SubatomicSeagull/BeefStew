import discord
from data import postgres
from beefcommands.invocations.joker_score.joker_registration import is_registered, register_user
from beefutilities.guilds import text_channel

async def retrieve_joke_score(user: discord.Member):
    joke_score = await (postgres.read(f"SELECT current_score FROM joke_scores WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';"))
    score = joke_score[0][0]
    return int(score)

# probably not going to use this
async def get_multilplier(user: discord.Member):
    winner = discord.utils.get(user.guild.roles, name="the funniest person ever")
    loser = discord.utils.get(user.guild.roles, name="tonights biggest loser")   
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
        print(e)
        await interaction.followup.send(f"couldnt find {user.name}'s score :( ({e}))")