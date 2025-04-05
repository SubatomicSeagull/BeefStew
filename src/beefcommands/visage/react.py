import discord
from PIL import Image, ImageEnhance, ImageOps
from io import BytesIO
import os
from beefutilities.IO import file_io
from data import postgres

async def react(interaction: discord.Interaction, message: discord.Message):
    try:
        reaction = await add_reaction(message)
        await interaction.response.send_message(content= "", file=discord.File(fp=reaction, filename=f"reaction.png"))
        
        # clear the bytesio buffer
        reaction.close()
        
    except Exception as e:
        postgres.log_error(e)
        await interaction.response.send_message(f"i dont think that worked sry :// for now its only pngs and jpgs lol", ephemeral=True)

async def get_attachment(message: discord.Message):
    if not message.attachments:
        return None
    attachment = next((image for image in message.attachments if image.content_type.endswith(('png', 'jpg', 'jpeg', 'gif'))), None)
    
    if attachment is None:
        return None
    return await attachment.read()


async def add_reaction(message: discord.Message):
    
    # scan the message for an attachement
    image = Image.open(BytesIO(await get_attachment(message)))
    image = image.convert("RGBA")
    
    # construct a file path to the assets folder and oipen reaction image
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