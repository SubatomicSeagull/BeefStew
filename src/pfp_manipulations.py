import discord
from discord.ext import commands
from PIL import Image, ImageOps
import requests
from io import BytesIO


async def get_victim_avatar(victim: discord.Member):  
    avatar_url = victim.display_avatar.url
    response = requests.get(avatar_url)
    user_pfp = Image.open(BytesIO(response.content))
    user_pfp = user_pfp.convert('RGBA')
    user_pfp = ImageOps.fit(user_pfp, (350, 350))
    return user_pfp

async def boil_pfp(victim: discord.Member):   
    avatar = await get_victim_avatar(victim)
    user_pfp = Image.new("RGBA", avatar.size, (255,255,255))
    user_pfp.paste(avatar, (0,0))
    # reading the boil template
    template = Image.open(".\\src\\assets\\pfp_manipulation\\boiling_pan_1.png")
    # creating the tint image
    tint = Image.new("RGBA",user_pfp.size, (255, 0, 0))
    # blending it with the pfp
    user_pfp = Image.blend(user_pfp, tint, 0.3)

    base_width, base_height = user_pfp.size
    overlay_width, overlay_height = template.size

    x = (overlay_width - base_width) // 2
    y = (overlay_height - base_height) // 2 - 75

    # generating the final image
    final_image = Image.new("RGBA", template.size, (255, 255, 255))
    # overlay the tinted pfp on the final image
    final_image.paste(user_pfp, (x,y))
    # overlay the template on the tinted pfp
    final_image.paste(template, (0,0), template)
    
    # write the image to BytesIO buffer
    image_binary = BytesIO()
    final_image.save(image_binary, 'PNG')
    image_binary.seek(0)
    return image_binary

async def add_speech_bubble(victim: discord.Member):
    user_pfp = await get_victim_avatar(victim)
    speech_bubble = Image.open(".\\src\\assets\\pfp_manipulation\\speechbubble.png")
    user_pfp.paste(speech_bubble, (0,0), speech_bubble)
    final_image = Image.new("RGBA", (user_pfp.size), (255,255,255))
    final_image.paste(user_pfp, (0,0))
    
    # write the image to BytesIO buffer
    image_binary = BytesIO()
    final_image.save(image_binary, 'PNG')
    image_binary.seek(0)
    return image_binary

async def drain_overlay(victim: discord.Member):
    avatar = await get_victim_avatar(victim)
    new_size = (int(avatar.width * 0.5), int(avatar.height * 0.5))
    user_pfp = avatar.resize(new_size, Image.Resampling.BILINEAR)
    
    template = Image.open(".\\src\\assets\\pfp_manipulation\\drain.png")

    base_width, base_height = user_pfp.size
    overlay_width, overlay_height = template.size

    x = (overlay_width - base_width) // 1 -200
    y = (overlay_height - base_height) // 1 -150

    final_image = Image.new("RGBA", template.size, (0, 0, 0))
    final_image.paste(user_pfp, (x,y))
    final_image.paste(template, (0,0), template)
    
    image_binary = BytesIO()
    final_image.save(image_binary, 'PNG')
    image_binary.seek(0)
    return image_binary
    