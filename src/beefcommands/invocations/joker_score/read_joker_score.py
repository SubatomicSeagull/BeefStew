import discord
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from data import postgres
from io import BytesIO
from beefcommands.invocations.joker_score.joker_registration import is_registered_users, is_registered_score, register_user, register_score
from beefutilities.users.user import get_average_avatar_color

async def retrieve_joke_score(user: discord.Member):
    if not await is_registered_users(user):
        await register_user(user)
        
    if not await is_registered_score(user):
        await register_score(user)
        
    joke_score = await (postgres.read(f"SELECT current_score FROM joke_scores WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';"))
    score = joke_score[0][0]
    return int(score)

async def get_user_highest_score(user: discord.Member):
    if not await is_registered_users(user):
        await register_user(user)
        
    if not await is_registered_score(user):
        await register_score(user)
        
    highest_score = await (postgres.read(f"SELECT highest_score FROM joke_scores WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';"))
    score = highest_score[0][0]
    return int(score)

async def get_user_lowest_score(user: discord.Member):
    if not await is_registered_users(user):
        await register_user(user)
        
    if not await is_registered_score(user):
        await register_score(user)
        
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
    if not await is_registered_users(user):
        await register_user(user)
        
    if not await is_registered_score(user):
        await register_score(user)
        
    try:
        score = await retrieve_joke_score(user)
        await interaction.followup.send(f"{user.mention}'s joker score: **{score}**!")
    except Exception as e:
        await interaction.followup.send(f"couldnt find {user.name}'s score :( ({e}))")

async def get_score_history(user: discord.Member):
    if not await is_registered_users(user):
        await register_user(user)

    if not await is_registered_score(user):
        await register_score(user)

    joker_score_id = await (postgres.read(f"SELECT id FROM public.joke_scores WHERE user_id = '{user.id}' AND guild_id = '{user.guild.id}';"))    
    x_axis = []
    y_axis = []
    
    #score_history_values = await (postgres.read(f"SELECT score_after FROM public.joke_scores_history WHERE joke_score_id = {joker_score_id[0][0]};"))
    #score_history_dates = await (postgres.read(f"SELECT date FROM public.joke_scores_history WHERE joke_score_id = {joker_score_id[0][0]};"))
    
    score_all = await (postgres.read(f"SELECT score_after, date FROM public.joke_scores_history WHERE joke_score_id = {joker_score_id[0][0]} ORDER BY date DESC LIMIT 30;"))
    
    for i in range (len(score_all)):
        y_axis.append(int(score_all[i][0]))
        x_axis.append(score_all[i][1])
        
    y_axis.reverse()
    x_axis.reverse()
        
    return x_axis, y_axis

async def generate_graph(user: discord.Member):

    x, y = await get_score_history(user)

    x_pos = list(range(len(x)))
    tick_positions = []
    tick_labels = []

    last_day = None

    for i, dt in enumerate(x):
        day = dt.date()
        if day != last_day:
            tick_positions.append(i)
            tick_labels.append(dt.strftime('%d/%m'))
            last_day = day

    fig, ax = plt.subplots()
    
    fig.patch.set_facecolor('#2b2b2b')
    ax.set_facecolor('#2b2b2b')

    x_pos = range(len(x))

    ax.plot(x_pos, y, marker='o', color=await get_average_avatar_color(user), linewidth=2, markersize=6)

    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, rotation=45, ha='right', color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    
    y_min = min(y)
    y_max = max(y)

    padding = max(2, int((y_max - y_min) * 0.2))

    ax.set_ylim(y_min - padding, y_max + padding)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    

    ax.set_xlabel('Date', color='white')
    ax.set_ylabel('Joker Score', color='white')
    ax.set_title(f'Joker Score History for {user.name}', color='white')
    ax.margins(x=0)

    for spine in ax.spines.values():
        spine.set_color('white')
    
    plt.axhline(0, color='white', linewidth=0.8, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    
    # write to the image binary and return
    image_binary = BytesIO()
    plt.savefig(image_binary, format='png', dpi=150, bbox_inches='tight')
    image_binary.seek(0)
    
    plt.close(fig)
    
    return image_binary

async def show_history(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer()

    # dm restriction
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send("we are literally in DMs rn bro u cant do that here...")
        return
    try:
        graph = await generate_graph(user)
        await interaction.followup.send(file = discord.File(fp = graph, filename = f"{user.name}_joker_score_history.png"))
        return
    except Exception as e:
        await interaction.followup.send(f"couldnt generate {user.name}'s score history :( ({e})")
        return