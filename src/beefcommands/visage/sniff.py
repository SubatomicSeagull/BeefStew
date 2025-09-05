import discord
from PIL import Image
from io import BytesIO
from beefutilities.users.user import get_avatar_image
from beefutilities.IO import file_io
from data import postgres

async def sniff_overlay(victim: discord.Member):
    #retrieve the users pfp and resize
    avatar = await get_avatar_image(victim)
    new_size = (int(avatar.width * 2), int(avatar.height * 2))
    user_pfp = avatar.resize(new_size, Image.Resampling.BILINEAR)

    # construct a file path to the assets folder
    template = Image.open(file_io.construct_assets_path("pfp_manipulation/beefsniff.png"))

    # resize the template
    base_width, base_height = user_pfp.size
    overlay_width, overlay_height = template.size

    # define the overlay coordinates and size
    x = (overlay_width - base_width) // 1 -700
    y = (overlay_height - base_height) // 1 + 20

    # compose the new image
    final_image = Image.new("RGBA", template.size, (255, 255, 255))
    final_image.paste(user_pfp, (x,y))
    final_image.paste(template, (0,0), template)


    # write the image binary buffer and return
    image_binary = BytesIO()
    final_image.save(image_binary, 'PNG')
    image_binary.seek(0)
    return image_binary

# usage of the above
async def sniff_user(interaction: discord.Interaction, victim: discord.Member):
    await interaction.response.defer()
    try:
        drain_pfp = await sniff_overlay(victim)
        await interaction.followup.send(content= f"Beefstew will remember your scent...", file=discord.File(fp=drain_pfp, filename=f"{victim.name}_sniff.png"))

        # clear the bytesio buffer
        drain_pfp.close()
    except Exception as e:
        postgres.log_error(e)
        await interaction.followup.send(f"{interaction.user.mention} tried to sniff {victim.name} but it didnt work :// ({e})")