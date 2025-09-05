from io import BytesIO
import discord
from beefutilities.IO import file_io
from PIL import Image, ImageOps, ImageSequence
from beefutilities.IO.file_io import fetch_from_source


async def generate_explode_gif(image: Image.Image):
    overlay_path = file_io.construct_assets_path("pfp_manipulation", "explode.gif")
    overlay = Image.open(overlay_path)
    frames = []

    max_size = 600

    if image.width > max_size or image.height > max_size:
        print(f"resizing image from {image.width}x{image.height}")
        image.thumbnail((max_size, max_size), Image.LANCZOS)
        print(f"to {image.width}x{image.height}")

    for i, frame in enumerate(ImageSequence.Iterator(overlay)):
        if i % 2 == 0:
            continue
        new_frame = ImageOps.fit(frame.convert("RGBA"), image.size)
        composite = image.copy()
        composite.paste(new_frame, (0, 0), new_frame)
        frames.append(composite.convert("P", palette=Image.ADAPTIVE, dither=Image.NONE))


    image_binary = BytesIO()
    frames[0].save(
        image_binary,
        format="GIF",
        append_images=frames[1:],
        duration=100,
        loop=0,
        save_all=True,
        optimize=True,
        disposal=2
    )
    image_binary.seek(0)
    return image_binary

async def explode_img(interaction: discord.Interaction, source):
    await interaction.response.defer()

    try:
        image = await fetch_from_source(source)
        exploded = await generate_explode_gif(image)
        await interaction.followup.send(file=discord.File(fp=exploded, filename=f"exploded.gif"))
        exploded.close()
    except discord.HTTPException as e:
        await interaction.followup.send(f"file too big sorry :(")
    except AttributeError as e:
        await interaction.followup.send(f"that didnt work sry :// gotta be png or jpg")
    except Exception as e:
        await interaction.followup.send(f"uhhhhhhh something went wrong.... ({e})")