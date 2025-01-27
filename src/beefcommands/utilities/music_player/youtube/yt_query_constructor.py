import discord
import yt_dlp
import urllib
import re
import requests

async def get_metadata_yt(interaction: discord.Interaction, url: str):
    print("getting yt metadata")
    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
        'cookiefile': "C:\\Users\\subat\\Desktop\\BeefStew\\src\\beefcommands\\utilities\\music_player\\cookies.txt"
        }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict
    
async def yt_search_term(interaction: discord.Interaction, search_term: str):
    print(f"searching youtube for \"{search_term}\"...")
    phrase = search_term.replace(" ", "+")
    search_link = "https://www.youtube.com/results?search_query=" + phrase
    response = urllib.request.urlopen(search_link)
    
    search_results = re.findall(r'watch\?v=(\S{11})', response.read().decode())
    first_result = search_results[0]
    url = "https://www.youtube.com/watch?v=" + first_result
    return await get_metadata_yt(interaction, url)