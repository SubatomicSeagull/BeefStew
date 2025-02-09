import discord
from PIL import Image
from io import BytesIO
import os
from beefutilities.user import get_avatar_image
from data import postgres

async def add_speech_bubble_pfp(victim: discord.Member):
    # retrive the users pfp
    user_pfp = await get_avatar_image(victim)
    
    # cnstruct a file path to the assets folder
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, '..', '..')
    speech_bubble = Image.open(os.path.join(file_path, "assets", "pfp_manipulation", "speechbubble.png"))
    
    # paste the speech bubble templte over the image
    user_pfp.paste(speech_bubble, (0,0), speech_bubble)
    
    # compise the final image over the new one
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
        await interaction.followup.send(file=discord.File(fp=slandered_pfp, filename=f"{victim.name} slandered.png"))
        
        # clear the bytesio buffer
        slandered_pfp.close()
    except Exception as e:
        postgres.log_error(e)
        print(e)
        await interaction.followup.send(content=f"{interaction.user.mention} tried to slander {victim.mention}, but it didnt work :// ({e})")
    