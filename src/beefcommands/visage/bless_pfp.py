import discord
from PIL import Image
from io import BytesIO
import os
from beefutilities.user import get_avatar_image
from data import postgres

async def bless_pfp(victim: discord.Member):
    avatar = await get_avatar_image(victim)
    new_size = (int(avatar.width * 0.5), int(avatar.height * 0.5))
    user_pfp = avatar.resize(new_size, Image.Resampling.BILINEAR)
    user_pfp = user_pfp.rotate(30, resample=Image.BICUBIC, expand=True)
    
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, '..', '..')
    template = Image.open(os.path.join(file_path, "assets", "pfp_manipulation", "jesus.png"))
    
    base_width, base_height = user_pfp.size
    overlay_width, overlay_height = template.size

    x = (overlay_width - base_width) // 1 + 5
    y = (overlay_height - base_height) // 1 +20
    

    final_image = Image.new("RGBA", template.size, (255, 255, 255))
    final_image.paste(user_pfp, (x,y))
    final_image.paste(template, (0,0), template)
    
    image_binary = BytesIO()
    final_image.save(image_binary, 'PNG')
    image_binary.seek(0)
    return image_binary

async def bless(interaction: discord.Interaction, victim: discord.Member):
    await interaction.response.defer()
    try:
        jesus_pfp = await bless_pfp(victim)
        await interaction.channel.send(f"{victim.mention} bless you my child...")
        await interaction.followup.send(file=discord.File(fp=jesus_pfp, filename=f"{victim.name} with jesus.png"))
        jesus_pfp.close()
        
    except Exception as e:
        postgres.log_error(e)
        print(e)
        await interaction.followup.send(f"{interaction.user.mention} tried to find jesus {victim.name} but it didnt work :// ({e})")