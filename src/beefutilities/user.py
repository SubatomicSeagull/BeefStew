import discord
import requests
from PIL import Image, ImageOps
from io import BytesIO

async def get_avatar_image(victim: discord.Member):  
    avatar_url = await get_user_avatar(victim)
    response = requests.get(avatar_url)
    user_pfp = Image.open(BytesIO(response.content))
    user_pfp = user_pfp.convert('RGBA')
    user_pfp = ImageOps.fit(user_pfp, (350, 350))
    return user_pfp

async def get_user_avatar(user: discord.Member):
    return user.display_avatar.url