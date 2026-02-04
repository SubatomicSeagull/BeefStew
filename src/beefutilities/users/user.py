import discord
import requests
from PIL import Image, ImageOps, ImageEnhance
from io import BytesIO
from data import postgres
from beefcommands.invocations.joker_score.joker_registration import is_registered_users, register_user
import datetime
import aiohttp

async def get_avatar_image(victim: discord.Member):
    # retrieve the url of the users pfp
    avatar_url = await get_user_avatar(victim)
    response = requests.get(avatar_url)

    # write the pfp image to the image buffer and return
    user_pfp = Image.open(BytesIO(response.content))
    user_pfp = user_pfp.convert('RGBA')
    user_pfp = ImageOps.fit(user_pfp, (350, 350))
    return user_pfp

async def get_user_avatar(user: discord.Member):
    return user.display_avatar.url

async def get_average_avatar_color(user: discord.Member) -> str:
    
    url =  await get_user_avatar(user)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return "#ffcc00"

            data = await resp.read()

    img = Image.open(BytesIO(data)).convert("RGB")
    img = img.resize((50, 50))
    
    img = ImageEnhance.Color(img).enhance(2)
    pixels = list(img.getdata())
    r = sum(p[0] for p in pixels) // len(pixels)
    g = sum(p[1] for p in pixels) // len(pixels)
    b = sum(p[2] for p in pixels) // len(pixels)

    return f"#{r:02x}{g:02x}{b:02x}"


async def register_user_bday(user: discord.Member, birthday):
    # check if the user is already registered
    if not await is_registered_users(user):  # Added user.guild as the guild argument
        await register_user(user)

    try:
        bday = datetime.datetime.strptime(birthday, "%d/%m/%Y").date()
        await postgres.write(f"UPDATE users SET birthday = '{bday}' WHERE user_id = '{user.id}';")
        return f"ur birthday is now set to {bday.strftime('%d/%m/%Y')}"
    except ValueError:
        return "u have to format it like dd/mm/yyyy so like 11/09/2001"

async def set_msg_flag(user: discord.Member, flag: bool):
    # check if the user is already registered
    if not await is_registered_users(user):  # Added user.guild as the guild argument
        await register_user(user)

    # set the msg flag for the user
    try:
        await postgres.write(f"UPDATE users SET msg_flag = {flag} WHERE user_id = '{user.id}';")
        return "beefstew sniffed u"
    except Exception as e:
        return("beefstew doesnt wanna sniff u... " + e)
