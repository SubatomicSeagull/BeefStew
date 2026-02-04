import discord
from PIL import ImageOps
from io import BytesIO
from beefutilities.IO.file_io import fetch_from_source

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

    try:
        image = await fetch_from_source(source)
        mirrored = await mirror_img(image)
        await interaction.followup.send(file = discord.File(fp = mirrored, filename = f"mirrored.png"))
        mirrored.close()
    except discord.HTTPException as e:
        await interaction.followup.send(f"file too big sorry :(")
    except AttributeError as e:
        await interaction.followup.send(f"that didnt work sry :// gotta be an image")
    except Exception as e:
        await interaction.followup.send(f"uhhhhhhh something went wrong.... ({e})")