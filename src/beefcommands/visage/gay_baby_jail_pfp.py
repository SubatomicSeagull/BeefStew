import discord
from PIL import Image
from io import BytesIO
import os
from beefutilities.users.user import get_avatar_image
from beefutilities.IO import file_io
from data import postgres

async def gay_baby_jail_pfp(victim: discord.Member):
    # retrive the user pfp and resize
    avatar = await get_avatar_image(victim)
    new_size = (int(avatar.width * 0.4), int(avatar.height * 0.4))
    user_pfp = avatar.resize(new_size, Image.Resampling.BILINEAR)
    
    # construct a file path to the assets folder 
    template = Image.open(file_io.construct_assets_path("pfp_manipulation/GBJ.png"))
    
    # resize the template
    base_width, base_height = user_pfp.size
    overlay_width, overlay_height = template.size

    # define the template coordinates and scale
    x = (overlay_width - base_width) // 1 -100
    y = (overlay_height - base_height) // 1 -75

    # compose the new image
    final_image = Image.new("RGBA", template.size, (255, 255, 255))
    boxbg = Image.new("RGBA", [200,200], (75, 25, 0))
    final_image.paste(boxbg, (x-10,y-20))
    final_image.paste(user_pfp, (x,y))
    final_image.paste(template, (0,0), template)
    
    # write the image binary buffer and return
    image_binary = BytesIO()
    final_image.save(image_binary, 'PNG')
    image_binary.seek(0)
    return image_binary

# usage of the above
async def GBJ(interaction: discord.Interaction, victim: discord.Member):
    await interaction.response.defer()
    try:
        gbj_pfp = await gay_baby_jail_pfp(victim)
        await interaction.followup.send(content= f"{victim.mention} about time they locked that fucker away...", file=discord.File(fp=gbj_pfp, filename=f"{victim.name} jailed.png"))
        
        # clear the bytesio buffer.
        gbj_pfp.close()
        
    except Exception as e:
        postgres.log_error(e)
        await interaction.followup.send(f"{interaction.user.mention} tried to put {victim.name} in gay baby jail but it didnt work :// ({e})")