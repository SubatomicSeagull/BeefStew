import wikipediaapi
import requests
import discord
from beefutilities.IO import file_io
from beefutilities.TTS import speak


async def wikifetchpage(query):
    wiki = wikipediaapi.Wikipedia("BeefStew", "en")
    page = wiki.page(query)
    if not page.exists():
        url = "https://en.wikipedia.org/w/api.php"
        headers = {"User-Agent": "BeefStew"}
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json"
        }
        response = requests.get(url, headers=headers, params=params)
        print(response)
        data = response.json()
        
        try:
            if data["query"]["search"]:
                closest_match = data["query"]["search"][0]["title"]
                page = wiki.page(closest_match)
        except Exception as e:
            print(f"Error occurred: {e}")
            page = None
            return
    return page

async def tellme(message: discord.Message, query):
    if isinstance(message.channel, discord.DMChannel):
        await message.reply("we are literally in DMs rn bro u cant do that here...")
        return
    page = await wikifetchpage(query)
    
    if not page.exists():
        content = f"i dont know anything about {query} :("
        image = file_io.construct_media_path("idk_monkey.png")
        await message.reply(content=content, file=discord.File(fp=image, filename=f"beefstew doesnt know about {query}.png"))

    else:
        summary = (page.summary).split('. ')
        content = ""
        for sentence in summary:
            if len(content ) + len(sentence) + 2 > 1965:
                break
            if not content.endswith(('.', '!', '?')):
                content += ". "
            content += sentence
    await message.reply(content=f"<:nerdstew:1387429699625681090> {content}")
    await speak.speak_output(message, content)
    return