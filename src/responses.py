import json
import os
import random
import discord
from json_handling import load_element

def load_responses(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Construct the file path to responses.json
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'assets', 'responses.json')

responses = load_responses(file_path)

text_responses = responses['text_responses']
keyword_responses = responses['keyword_responses']
emoji_responses = responses['emoji_responses']

def get_response(message):
    message_text = str(message).lower()
    if not message_text:
        return ""

    response = ""

    # Check for exact text responses
    if message_text in text_responses:
        response += text_responses[message_text]

    # Check for keyword responses
    for keyword, keyword_response in keyword_responses.items():
        if keyword in message_text:
            response += keyword_response
            break

    # Append emoji responses in order of appearance
    for word in message_text.split():
        if word in emoji_responses:
            response += emoji_responses[word]

    return response


async def get_insult():
    with open(file_path, 'r') as file:
        data = json.load(file)
    insult = random.choice(data["insults"])
    return insult

async def vicious_mockery(interaction: discord.Interaction, victim: discord.Member):
    if victim.id != 1283805971524747304:
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