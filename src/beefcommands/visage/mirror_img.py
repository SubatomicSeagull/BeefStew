import discord
from PIL import Image, ImageEnhance, ImageOps
from io import BytesIO
import os
from beefutilities.IO.file_io import fetch_from_source
from beefutilities.IO import file_io
from data import postgres

async def mirror_img(img):
    
    # mirror the image centrally on the x-axis
    mirrored_part = ImageOps.mirror(img.crop((0, 0, img.width // 2, img.height)))
    img.paste(mirrored_part, (img.width // 2, 0))
    
    image_binary = BytesIO()
    img.save(image_binary, 'PNG')
    image_binary.seek(0)
    return image_binary


# usage of the above
async def mirror(interaction: discord.Interaction, source):
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
        mirrored_img = await mirror_img(src)
        await interaction.followup.send(content="", file=discord.File(fp=mirrored_img, filename=f"mirrored.png"))
        
        # clear the bytesio buffer
        mirrored_img.close()
    except Exception as e:
        await postgres.log_error(e)
        await interaction.followup.send(f"{e}")