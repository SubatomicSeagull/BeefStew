import json
import os
import discord
from json_handling import load_element

async def get_response(message: discord.Message):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'assets', 'responses.json')
    with open(file_path, "r") as file:
        responses = json.load(file)
    for trigger_phrase, response in responses["trigger_phrases"].items():
        if trigger_phrase in message.content.lower():
            response_type = response.get("type")
            content = response.get("content")
            if isinstance(response, dict) and response_type == "media":
                media_path = os.path.join(current_dir, 'assets', 'media', (content))
                await message.reply(file=discord.File(media_path))
                return
            else:
                await message.reply(content)
                return