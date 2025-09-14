import discord
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from io import BytesIO
from beefutilities.users.user import get_avatar_image
from beefutilities.IO import file_io

async def party_pfp(victim: discord.Member):
    # retrieve the user pfp and resize
    avatar = await get_avatar_image(victim)
    new_size = (int(avatar.width * 0.55), int(avatar.height * 0.55))
    user_pfp = avatar.resize(new_size, Image.Resampling.BILINEAR)

    # construct a file path to the assets folder
    template = Image.open(file_io.construct_assets_path("pfp_manipulation/birthday.png"))

    # resize the template
    base_width, base_height = user_pfp.size
    overlay_width, overlay_height = template.size

    # define the template coordinates and scale
    x = (overlay_width - base_width) // 1 -114
    y = (overlay_height - base_height) // 1 + 10

    # compose the new image
    final_image = Image.new("RGBA", template.size, (255, 255, 255))
    final_image.paste(user_pfp, (x,y))
    final_image.paste(template, (0,0), template)

    # add the red text over the top
    draw = ImageDraw.Draw(final_image)
    font = ImageFont.truetype(file_io.construct_assets_path("fonts/comic-sans-bold.ttf"), 19)
    draw.text((4, 260), f"Happy Birthday {victim.name}!", (255, 0, 0), font=font)

    # write the image binary buffer and return
    image_binary = BytesIO()
    final_image.save(image_binary, 'PNG')
    image_binary.seek(0)
    return image_binary