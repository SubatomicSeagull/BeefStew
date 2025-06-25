import requests
import os
import random
import discord

async def retrieve_image(query):
    # define params with api key secret and search engine id
    params = {"key": os.getenv("GOOGLEAPIKEY"), "cx": os.getenv("SEARCHENGINEID"), "q": query, "searchType": "image", "num": 6}

    # make the request to the google custom search api
    resp = requests.get("https://customsearch.googleapis.com/customsearch/v1", params=params)
    resp.raise_for_status()

    #extract thje image link from the response
    data = resp.json()
    items = data.get("items", [])
    links = [item["link"] for item in items]
    while links:
        index = random.randint(0, len(links) - 1)
        img = links.pop(index)
        if not "instagram" in img and not "crawler" in img:
            return img
    return "I had a look and i cant find it im sorry :("

async def show(message: discord.Message, query):
    if isinstance(message.channel, discord.DMChannel):
        await message.reply("we are literally in DMs rn bro u cant do that here...")
        return
    try:
        # retrieve the image link from the google custom search api
        image_link = await retrieve_image(query)
    except Exception as e:
        await message.reply(f"I had a look and i cant find it im sorry :( {e}")
        return
    
    # send the image link as a response to the interaction
    await message.reply(image_link)
    return
