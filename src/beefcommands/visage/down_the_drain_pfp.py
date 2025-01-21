import discord
from PIL import Image
from io import BytesIO
import os
from beefutilities.user import get_avatar_image
from data import postgres

async def drain_overlay(victim: discord.Member):
    avatar = await get_avatar_image(victim)
    new_size = (int(avatar.width * 0.5), int(avatar.height * 0.5))
    user_pfp = avatar.resize(new_size, Image.Resampling.BILINEAR)
    
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, '..', '..')
    template = Image.open(os.path.join(file_path, "assets", "pfp_manipulation", "drain.png"))

    base_width, base_height = user_pfp.size
    overlay_width, overlay_height = template.size

    x = (overlay_width - base_width) // 1 -200
    y = (overlay_height - base_height) // 1 -150

    final_image = Image.new("RGBA", template.size, (0, 0, 0))
    final_image.paste(user_pfp, (x,y))
    final_image.paste(template, (0,0), template)
    
    image_binary = BytesIO()
    final_image.save(image_binary, 'PNG')
    image_binary.seek(0)
    return image_binary

async def down_the_drain(interaction: discord.Interaction, victim: discord.Member):
    await interaction.response.defer()
    try:
        drain_pfp = await drain_overlay(victim)
        await interaction.channel.send(f"yeah sorry we dropped {victim.mention} in there we cant get them out ://")
        await interaction.followup.send(file=discord.File(fp=drain_pfp, filename=f"{victim.name} dropped down the drain.png"))
        drain_pfp.close()
    except Exception as e:
        postgres.log_error(e)
        print(e)
        await interaction.followup.send(f"{interaction.user.mention} tried to drop {victim.name} down the drain but it didnt work :// ({e})")