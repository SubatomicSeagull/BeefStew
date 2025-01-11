import json
import os
import random
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
        
async def get_insult():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'assets', 'responses.json')
    with open(file_path, 'r') as file:
        data = json.load(file)
    insult = random.choice(data["insults"])
    return insult

async def vicious_mockery(interaction: discord.Interaction, victim: discord.Member):
    if victim.id != os.getenv("CLIENTID"):
        try:
            insult = await get_insult()
            if victim.id == interaction.user.id:
                return(f"{interaction.user.mention} tried to cast Vicious Mockery on themselves for some reason...\nit still works tho, {interaction.user.mention} {insult} ")
            else:
                return(f"{victim.mention} {insult}")
        except Exception as e:
            return (f"{interaction.user.mention} tried to cast Vicious Mockery on {victim.mention}... but it failed ({e})")
    else:
        return(f"{interaction.user.mention} tried to cast Vicious Mockery on me...BITCH")
    
async def get_joke_response_positive(member: discord.Member):     
    jokertag = type('Joker', (object,), {"mention": member.mention})()
    responses = load_element("responses.json", "joke_responses_positive")
        
    chosen_response = random.choice(responses)
    chosen_response = chosen_response.format(joker=jokertag)
    return chosen_response

async def get_joke_response_negative( member: discord.Member):     
    jokertag = type('Joker', (object,), {"mention": member.mention})()
    responses = load_element("responses.json", "joke_responses_negative")
        
    chosen_response = random.choice(responses)
    chosen_response = chosen_response.format(joker=jokertag)
    return chosen_response