import json
import os
import random
import discord

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
    with open("src\\assets\\responses.json", 'r') as file:
        data = json.load(file)
    insult = random.choice(data["insults"])
    return insult


#async def helpembed(thumbnail):
#    
#    embed = discord.Embed(
#        title="Beefstew Help",
#        description="You don't want to know what I can *really* do...",
#        color=discord.Color.lighter_grey()
#    )
#    embed.set_thumbnail(url=thumbnail)
#    embed.add_field(name="Commands:",value="", inline=False)
#    embed.add_field(name="",value="`/help 1` -  **Moderation** commands list", inline=False)
#    embed.add_field(name="",value="`/help 2` - **Utilities** commands list", inline=False)
#
#
#
#    embed.add_field(name="\nOther info:\n",value="", inline=False)
#    embed.add_field(name="", value="Privacy Policy", inline=True)
#    embed.add_field(name="", value="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Terms of Service", inline=True)
#    embed.add_field(name="", value="[cosycraft.uk/privacy](https://www.cosycraft.uk/privacy)⠀⠀⠀⠀⠀⠀⠀[cosycraft/tos](https://www.cosycraft.com/tos)", inline=False)
  
    
#   return embed