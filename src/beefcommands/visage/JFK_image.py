import discord
from PIL import Image, ImageEnhance, ImageOps
from io import BytesIO
import os
from beefutilities.IO.file_io import fetch_from_source
from beefutilities.IO import file_io
from data import postgres

async def jfk(img):
    
    new_size = (int(img.width * 0.2), int(img.height * 0.2))
    img = img.resize(new_size, Image.Resampling.BILINEAR)
    
    # make the pfp grayscale by setting saturation to 0
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(0)
    
    # construct a file path to the assets folder
    template = Image.open(file_io.construct_assets_path("pfp_manipulation/jfk.png"))
    
    # resize the template
    base_width, base_height = img.size
    overlay_width, overlay_height = template.size

    # define the overlay coodinates and scale
    x = (overlay_width - base_width) // 1 -162
    y = (overlay_height - base_height) // 1 -80
    
    # compose the final image
    final_image = Image.new("RGBA", template.size, (255, 255, 255))
    final_image.paste(img, (x,y))
    final_image.paste(template, (0,0), template)
    
    # write to the image binary buffer
    image_binary = BytesIO()
    final_image.save(image_binary, 'PNG')
    image_binary.seek(0)
    return image_binary

# usage of the above 
async def watch_out(interaction: discord.Interaction, source):
    await interaction.response.defer()
    
    #retrive the image bytes from source, either a user or an attachment
    try:
        src = await fetch_from_source(source)
        if src is None:
            await interaction.followup.send(f"i dont think that worked sry :// for now its only pngs and jpgs lol", ephemeral=True)
            return
        src = ImageOps.fit(src, (350, 350))
    except Exception as e:
        await postgres.log_error(e)
        await interaction.followup.send(f"i dont think that worked sry :// for now its only pngs and jpgs lol", ephemeral=True)
        return

    img = Image.new("RGBA", src.size, (255,255,255))
    img.paste(src, (0,0))

    try:
        boiled_img = await jfk(src)
        await interaction.followup.send(content="", file=discord.File(fp=boiled_img, filename=f"watch out.png"))
        
        # clear the bytesio buffer
        boiled_img.close()
    except Exception as e:
        await postgres.log_error(e)
        await interaction.followup.send(f"{e}")