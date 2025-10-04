import os
import discord
import aiohttp
import re
from io import BytesIO
from PIL import Image
from beefutilities.users.user import get_avatar_image


def construct_file_path(*args):
    return os.path.join((os.path.dirname(__file__)), "..", "..", *args)

def construct_assets_path(*args):
        return os.path.join((os.path.dirname(__file__)), "..", "..", "assets", *args)

def construct_media_path(*args):
    return os.path.join((os.path.dirname(__file__)), "..", "..", "assets", "media", *args)

def construct_root_path(*args):
    return os.path.join((os.path.dirname(__file__)), "..", "..", "..", *args)

def construct_data_path(*args):
    return os.path.join((os.path.dirname(__file__)), "..", "..", "data", *args)

# loop through attachments and find only image files, TODO add support for other images like .heic, webp, tiff, convert these to png before processing
async def get_attachment(message: discord.Message):
    if not message.attachments:
        url_pattern = re.compile("https?://\S+")
        urls = url_pattern.findall(message.content or "")
        for url in urls:
            lower = url.lower().split("?")[0]
            if any(lower.endswith(ext) for ext in ['png', 'jpg', 'jpeg', 'gif']):
                return await image_bytes(url)
    else:
        attachment = next((image for image in message.attachments if image.content_type.endswith(('png', 'jpg', 'jpeg', 'gif'))), None)
        return await attachment.read()

async def image_bytes(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()

# fetch an image from a link, either a discotrd user avatar url or a link in a message
async def fetch_from_source(source):
    if isinstance(source, discord.Member):
        src = await get_avatar_image(source)
    else:
        attachment = await get_attachment(source)
        try:
            src = Image.open(BytesIO(attachment))
            src = src.convert('RGBA')
        except Exception as e:
            return None
    return src
