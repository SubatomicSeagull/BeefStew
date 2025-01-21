import discord
from PIL import Image
from io import BytesIO
import os
from beefutilities.user import get_avatar_image
from data import postgres

async def boil_pfp(victim: discord.Member):   
    avatar = await get_avatar_image(victim)
    user_pfp = Image.new("RGBA", avatar.size, (255,255,255))
    user_pfp.paste(avatar, (0,0))

    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, '..', '..')
    template = Image.open(os.path.join(file_path, "assets", "pfp_manipulation", "boiling_pan_1.png"))
    
    tint = Image.new("RGBA",user_pfp.size, (255, 0, 0))
    user_pfp = Image.blend(user_pfp, tint, 0.3)

    base_width, base_height = user_pfp.size
    overlay_width, overlay_height = template.size

    x = (overlay_width - base_width) // 2
    y = (overlay_height - base_height) // 2 - 75

    final_image = Image.new("RGBA", template.size, (255, 255, 255))
    final_image.paste(user_pfp, (x,y))
    final_image.paste(template, (0,0), template)
    
    image_binary = BytesIO()
    final_image.save(image_binary, 'PNG')
    image_binary.seek(0)
    return image_binary

async def boil(interaction: discord.Interaction, victim: discord.Member):
    await interaction.response.defer()
    try:
        boiled_pfp = await boil_pfp(victim)
        await interaction.followup.send(file=discord.File(fp=boiled_pfp, filename=f"{victim.name} boiled.png"))
        await interaction.channel.send(f"{victim.mention} WAS BOILED!!!!")
        boiled_pfp.close()
    except Exception as e:
        await postgres.log_error(e)
        print(e)
        await interaction.followup.send(f"{interaction.user.mention} tried to boil {victim.name} but it didnt work :// ({e})")