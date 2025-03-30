import discord
import os
import datetime
from beefutilities.IO import file_io
from beefutilities.guilds.text_channel import read_guild_info_channel

async def image_of_the_day(bot):
    today = str(datetime.datetime.now().date().month) + "-" + str(datetime.datetime.now().date().day)
    dotw = str(datetime.datetime.now().date().strftime("%A") + "-" + str(datetime.datetime.now().date().day)).lower()   
    for image in os.listdir(file_io.construct_assets_path("IOTD")):
        imagename = os.path.splitext(image)[0]
        if imagename == today:
            await send_image_of_the_day(bot, image)
        if imagename == dotw:
            await send_image_of_the_day(bot, image)
            
async def send_image_of_the_day(bot, image):
    guild = await bot.fetch_guild(1015579904005386250)
    channel = bot.fetch_channel(await read_guild_info_channel(guild.id))
    channel.send(content=f"", file=discord.File(fp=file_io.construct_assets_path(f"IOTD/{image}"), filename=image))