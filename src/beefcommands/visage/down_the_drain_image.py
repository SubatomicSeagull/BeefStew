import discord
from PIL import Image, ImageOps
from io import BytesIO
from beefutilities.IO import file_io
from beefutilities.IO.file_io import fetch_from_source

async def drain_overlay(img):
    template = Image.open(file_io.construct_assets_path("pfp_manipulation/drain.png"))

    new_size = (int(img.width * 0.5), int(img.height * 0.5))
    img = img.resize(new_size, Image.Resampling.BILINEAR)

    # resize the template
    base_width, base_height = img.size
    overlay_width, overlay_height = template.size

    # define the overlay coordinates and size
    x = (overlay_width - base_width) // 1 -200
    y = (overlay_height - base_height) // 1 -150

    # compose the final image
    final_image = Image.new("RGBA", template.size, (0, 0, 0))
    final_image.paste(img, (x,y))
    final_image.paste(template, (0,0), template)

    # write to the image binary buffer and return
    image_binary = BytesIO()
    final_image.save(image_binary, 'PNG')
    image_binary.seek(0)
    return image_binary

# usage of the above
async def drain(interaction: discord.Interaction, source):
    await interaction.response.defer()

    try:
        image = await fetch_from_source(source)
        image = ImageOps.fit(image, (255, 255))

        drain = await drain_overlay(image)
        await interaction.followup.send(file = discord.File(fp = drain, filename = f"down the drain.png"))
        drain.close()
    except discord.HTTPException as e:
        await interaction.followup.send(f"file too big sorry :(")
    except AttributeError as e:
        await interaction.followup.send(f"that didnt work sry :// gotta be an image")
    except Exception as e:
        await interaction.followup.send(f"uhhhhhhh something went wrong.... ({e})")