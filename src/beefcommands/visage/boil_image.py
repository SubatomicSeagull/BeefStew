import discord
from PIL import Image, ImageOps
from io import BytesIO
from beefutilities.IO import file_io
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

    try:
        image = await fetch_from_source(source)
        image = ImageOps.fit(image, (350, 350))

        boiled = await boil_img(image)
        await interaction.followup.send(file = discord.File(fp = boiled, filename = f"boiled.png"))
        boiled.close()
    except discord.HTTPException as e:
        await interaction.followup.send(f"file too big sorry :(")
    except AttributeError as e:
        await interaction.followup.send(f"that didnt work sry :// gotta be png or jpg")
    except Exception as e:
        await interaction.followup.send(f"uhhhhhhh something went wrong.... ({e})")
