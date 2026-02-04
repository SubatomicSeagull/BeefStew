import discord
from PIL import Image
from io import BytesIO
from beefutilities.users.user import get_avatar_image
from beefutilities.IO import file_io

async def add_speech_bubble_pfp(victim: discord.Member):
    # retrieve the users pfp
    user_pfp = await get_avatar_image(victim)

    # construct a file path to the assets folder
    speech_bubble = Image.open(file_io.construct_assets_path("pfp_manipulation/speechbubble.png"))


    # paste the speech bubble templte over the image
    user_pfp.paste(speech_bubble, (0,0), speech_bubble)

    # compile the final image over the new one
    final_image = Image.new("RGBA", (user_pfp.size), (255,255,255))
    final_image.paste(user_pfp, (0,0))

    # write to the image binary buffer
    image_binary = BytesIO()

    # save and return the image
    final_image.save(image_binary, 'PNG')
    image_binary.seek(0)
    return image_binary

# usage of the above
async def slander(interaction: discord.Interaction, victim: discord.Member):
    await interaction.response.defer()
    try:
        slandered_pfp = await add_speech_bubble_pfp(victim)
        await interaction.followup.send(file = discord.File(fp = slandered_pfp, filename = f"{victim.name} slandered.png"))

        slandered_pfp.close()

    except discord.HTTPException as e:
        await interaction.followup.send(f"file too big sorry :(")
    except AttributeError as e:
        await interaction.followup.send(f"that didnt work sry :// gotta be an image")
    except Exception as e:
        await interaction.followup.send(f"uhhhhhhh something went wrong.... ({e})")