import discord
from PIL import Image, ImageOps
from io import BytesIO
import os
from beefutilities.IO import file_io
from data import postgres
from beefutilities.IO.file_io import fetch_from_source

async def boil_img(img):
    # construct a file path to the assets folder
    template = Image.open(file_io.construct_assets_path("pfp_manipulation/boiling_pan_1.png"))
    
    # create the tint overlay
    tint = Image.new("RGBA",img.size, (255, 0, 0))
    img = Image.blend(img, tint, 0.3)

    # resize the template
    base_width, base_height = img.size
    overlay_width, overlay_height = template.size

    # define overlay coordinates and size
    x = (overlay_width - base_width) // 2
    y = (overlay_height - base_height) // 2 - 75

    # compose the final image
    final_image = Image.new("RGBA", template.size, (255, 255, 255))
    final_image.paste(img, (x,y))
    final_image.paste(template, (0,0), template)
    
    # write to the image binary and return
    image_binary = BytesIO()
    final_image.save(image_binary, 'PNG')
    image_binary.seek(0)
    return image_binary

# usage of the above
async def boil(interaction: discord.Interaction, source):
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


    img = Image.new("RGBA", src.size, (255,255,255))
    img.paste(src, (0,0))

    try:
        boiled_img = await boil_img(src)
        await interaction.followup.send(content="", file=discord.File(fp=boiled_img, filename=f"boiled.png"))
        
        # clear the bytesio buffer
        boiled_img.close()
    except Exception as e:
        await postgres.log_error(e)
        await interaction.followup.send(f"{e}")
