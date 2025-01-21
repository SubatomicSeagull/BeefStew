import discord
from PIL import Image
from io import BytesIO
import os
from beefutilities.user import get_avatar_image
from data import postgres

async def add_speech_bubble_pfp(victim: discord.Member):
    
    user_pfp = await get_avatar_image(victim)
    
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, '..', '..')
    speech_bubble = Image.open(os.path.join(file_path, "assets", "pfp_manipulation", "speechbubble.png"))
    
    user_pfp.paste(speech_bubble, (0,0), speech_bubble)
    final_image = Image.new("RGBA", (user_pfp.size), (255,255,255))
    final_image.paste(user_pfp, (0,0))
    image_binary = BytesIO()
    final_image.save(image_binary, 'PNG')
    image_binary.seek(0)
    return image_binary

async def slander(interaction: discord.Interaction, victim: discord.Member):   
    await interaction.response.defer()
    try:
        slandered_pfp = await add_speech_bubble_pfp(victim)
        await interaction.followup.send(file=discord.File(fp=slandered_pfp, filename=f"{victim.name} slandered.png"))
        slandered_pfp.close()
    except Exception as e:
        postgres.log_error(e)
        print(e)
        await interaction.followup.send(content=f"{interaction.user.mention} tried to slander {victim.mention}, but it didnt work :// ({e})")
    