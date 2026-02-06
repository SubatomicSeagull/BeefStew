import json
import os
import discord
import math
from beefcommands.invocations.joker_score.change_joker_score import change_joke_score
from beefutilities.users import user
from data import postgres
from beefutilities.IO import file_io
from PIL import Image, ImageSequence
from io import BytesIO
import asyncio

def load_swears():
    swears = []
    file_path = file_io.construct_assets_path('responses.json')
    with open(file_path, "r") as file:
        swears = json.load(file)["swears"]
    return swears


async def swear_jar_penalty(victim: discord.Member):
    # take 2 points from the victim and give it to the jar
    await change_joke_score(victim, victim, -2, "swear jar penalty")
    await postgres.write(f"UPDATE public.joke_scores SET current_score = current_score + 2 WHERE user_id = '99' AND guild_id = '{victim.guild.id}';")

async def get_swear_jar_score(guild: discord.Guild):
    joke_score = await (postgres.read(f"SELECT current_score FROM public.joke_scores WHERE user_id = '99' AND guild_id = '{guild.id}';"))
    score = joke_score[0][0]
    return score

async def empty_swear_jar(guild: discord.Guild):
    # take all the points from the jar and put it into the saint word payout
    score = await get_swear_jar_score(guild)
    await postgres.write(f"UPDATE public.joke_scores SET current_score = 0 WHERE user_id = '99' AND guild_id = '{guild.id}';")
    return score

async def swear_jar_payout(victims: list[discord.Member]):
    # tget the score in the jar, divide it by the number of victims, rounded up to the nearest integer
    scoreamount = math.ceil((await get_swear_jar_score(victims[0].guild))/len(victims))
    
    for victim in victims:
        await change_joke_score(await victim.guild.fetch_member(os.getenv("CLIENTID")), victim, scoreamount, "swear jar payout")
    await empty_swear_jar(victims[0].guild)
    
async def swear_jar_payout_embed(interaction: discord.Interaction, victims: list[discord.Member]):
    await interaction.response.defer()
    gif = await generate_payout_gif(victims)
    await interaction.followup.send(content="swear jar payout!!!", file=discord.File(fp=gif, filename="payout.gif"))
    return


async def generate_payout_gif(victims: list[discord.Member]):
    bg = Image.open(file_io.construct_media_path("payout.gif"))
    victim_images = await asyncio.gather(*(user.get_avatar_image(v) for v in victims))

    row = await center_row(victim_images, bg.width, 64, 5)
    x = (bg.width - row.width) // 2
    y = (bg.height - row.height) // 2 + 100

    frames = []
    durations = []

    for frame in ImageSequence.Iterator(bg):
        frame = frame.convert("RGBA")
        frame.paste(row, (x, y), row)
        frames.append(frame)
        durations.append(frame.info.get("duration", 40))

    final = BytesIO()
    frames[0].save(final, format="GIF", save_all=True, append_images=frames[1:], duration=durations, loop=bg.info.get("loop", 0), disposal=2, optimize=False)
    final.seek(0)
    return final


async def center_row(images, canvas_width, target_size=96, padding=8):

    n = len(images)
    if n == 0:
        raise ValueError("No images provided")

    n = min(n, 4)

    total_padding = padding * (n - 1)
    max_row_width = n * target_size + total_padding

    # only scale DOWN if needed
    scale = min(1.0, canvas_width / max_row_width)
    size = int(target_size * scale)

    row_width = n * size + total_padding
    row = Image.new("RGBA", (row_width, size), (0, 0, 0, 0))

    x = 0
    for img in images[:n]:
        avatar = img.convert("RGBA").resize((size, size), Image.LANCZOS)
        row.paste(avatar, (x, 0))
        x += size + padding

    return row

