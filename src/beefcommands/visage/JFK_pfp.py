import discord
from PIL import Image, ImageEnhance
from io import BytesIO
import os
from beefutilities.users.user import get_avatar_image
from beefutilities.IO import file_io
from data import postgres

async def jfk(victim: discord.Member):
    # retruve the users pfp and return
    avatar = await get_avatar_image(victim)
    new_size = (int(avatar.width * 0.2), int(avatar.height * 0.2))
    user_pfp = avatar.resize(new_size, Image.Resampling.BILINEAR)
    
    # make the pfp grayscale by setting saturation to 0
    enhancer = ImageEnhance.Color(user_pfp)
    user_pfp = enhancer.enhance(0)
    
    # construct a file path to the assets folder
    template = Image.open(file_io.construct_assets_path("pfp_manipulation/jfk.png"))
    
    # resize the template
    base_width, base_height = user_pfp.size
    overlay_width, overlay_height = template.size

    # define the overlay coodinates and scale
    x = (overlay_width - base_width) // 1 -162
    y = (overlay_height - base_height) // 1 -80
    
    # compose the final image
    final_image = Image.new("RGBA", template.size, (255, 255, 255))
    final_image.paste(user_pfp, (x,y))
    final_image.paste(template, (0,0), template)
    
    # write to the image binary buffer
    image_binary = BytesIO()
    final_image.save(image_binary, 'PNG')
    image_binary.seek(0)
    return image_binary

# usage of the above 
async def watch_out(interaction: discord.Interaction, victim: discord.Member):
    await interaction.response.defer()
    try:
        jfk_pfp = await jfk(victim)
        await interaction.followup.send(content= f"{victim.mention} MR PRESIDENT GET DOWN!!!!!!", file=discord.File(fp=jfk_pfp, filename=f"{victim.name} is jfk.png"))
        
        # clear the bytesio buffer
        jfk_pfp.close()
        
    except Exception as e:
        postgres.log_error(e)
        await interaction.followup.send(f"{interaction.user.mention} tried to put {victim.name} in gay baby jail but it didnt work :// ({e})")