import discord
from PIL import Image
from io import BytesIO
from beefutilities.IO import file_io
from beefutilities.IO.file_io import fetch_from_source

async def react(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.defer()

    try:
        image = await fetch_from_source(message)
        reacted = await add_reaction(image)
        await interaction.followup.send(file = discord.File(fp = reacted, filename = f"reacted.png"))
        reacted.close()
    except discord.HTTPException as e:
        await interaction.followup.send(f"file too big sorry :(")
    except AttributeError as e:
        await interaction.followup.send(f"that didnt work sry :// gotta be png or jpg")
    except Exception as e:
        await interaction.followup.send(f"uhhhhhhh something went wrong.... ({e})")

async def add_reaction(image):
    # construct a file path to the assets folder and open reaction image
    reaction = Image.open(file_io.construct_assets_path("pfp_manipulation/react.png"))

    # resize the reaction image to fit the base image
    base_width = image.width // 4
    w_percent = base_width / float(reaction.width)
    new_height = int(float(reaction.height) * w_percent)
    reaction = reaction.resize((base_width, new_height), Image.Resampling.BILINEAR)

    # compose the new image
    final_image = Image.new("RGBA", (image.size), (255,255,255))
    image.paste(reaction, (0,0),)
    final_image.paste(image, (0,0), image)

    # write the image binary buffer and return
    image_binary = BytesIO()
    final_image.save(image_binary, 'PNG')
    image_binary.seek(0)
    return image_binary