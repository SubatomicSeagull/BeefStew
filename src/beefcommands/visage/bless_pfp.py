import discord
from PIL import Image
from io import BytesIO
import os
from beefutilities.user import get_avatar_image
from data import postgres

async def bless_pfp(victim: discord.Member):
    # retrive the user pfp
    avatar = await get_avatar_image(victim)
    
    # resize the pfp
    new_size = (int(avatar.width * 0.5), int(avatar.height * 0.5))
    user_pfp = avatar.resize(new_size, Image.Resampling.BILINEAR)
    
    # rotate it 30 degrees clockwise
    user_pfp = user_pfp.rotate(30, resample=Image.BICUBIC, expand=True)
    
    # construct a file path to the assets folder
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, '..', '..')
    template = Image.open(os.path.join(file_path, "assets", "pfp_manipulation", "jesus.png"))
    
    # define the overlay to be the same size as the template
    base_width, base_height = user_pfp.size
    overlay_width, overlay_height = template.size

    # define the overlay coordinates and size
    x = (overlay_width - base_width) // 1 + 5
    y = (overlay_height - base_height) // 1 +20
    
    # compose the final imahe
    final_image = Image.new("RGBA", template.size, (255, 255, 255))
    final_image.paste(user_pfp, (x,y))
    final_image.paste(template, (0,0), template)
    
    # write to he image binary buffer and return
    image_binary = BytesIO()
    final_image.save(image_binary, 'PNG')
    image_binary.seek(0)
    return image_binary

# usage of the above
async def bless(interaction: discord.Interaction, victim: discord.Member):
    await interaction.response.defer()
    try:
        jesus_pfp = await bless_pfp(victim)
        await interaction.channel.send(f"{victim.mention} bless you my child...")
        await interaction.followup.send(file=discord.File(fp=jesus_pfp, filename=f"{victim.name} with jesus.png"))
        
        # clear the bytesio buffer
        jesus_pfp.close()
        
    except Exception as e:
        postgres.log_error(e)
        await interaction.followup.send(f"{interaction.user.mention} tried to find jesus {victim.name} but it didnt work :// ({e})")