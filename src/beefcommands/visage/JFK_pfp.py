import discord
from PIL import Image, ImageEnhance
from io import BytesIO
import os
from beefutilities.user import get_avatar_image
from data import postgres

async def jfk(victim: discord.Member):
    avatar = await get_avatar_image(victim)
    new_size = (int(avatar.width * 0.2), int(avatar.height * 0.2))
    user_pfp = avatar.resize(new_size, Image.Resampling.BILINEAR)
    
    enhancer = ImageEnhance.Color(user_pfp)
    user_pfp = enhancer.enhance(0)
    
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, '..', '..')
    template = Image.open(os.path.join(file_path, "assets", "pfp_manipulation", "jfk.png"))
    
    base_width, base_height = user_pfp.size
    overlay_width, overlay_height = template.size

    x = (overlay_width - base_width) // 1 -162
    y = (overlay_height - base_height) // 1 -80
    

    final_image = Image.new("RGBA", template.size, (255, 255, 255))
    final_image.paste(user_pfp, (x,y))
    final_image.paste(template, (0,0), template)
    
    
    image_binary = BytesIO()
    final_image.save(image_binary, 'PNG')
    image_binary.seek(0)
    return image_binary

async def watch_out(interaction: discord.Interaction, victim: discord.Member):
    await interaction.response.defer()
    try:
        jfk_pfp = await jfk(victim)
        await interaction.channel.send(f"{victim.mention} MR PRESIDENT GET DOWN!!!!!!")
        await interaction.followup.send(file=discord.File(fp=jfk_pfp, filename=f"{victim.name} is jfk.png"))
        jfk_pfp.close()
        
    except Exception as e:
        postgres.log_error(e)
        print(e)
        await interaction.followup.send(f"{interaction.user.mention} tried to put {victim.name} in gay baby jail but it didnt work :// ({e})")