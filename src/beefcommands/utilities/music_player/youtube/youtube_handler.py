import requests
import re
import html
import yt_dlp
import urllib.request
import urllib.parse
import asyncio
from main import asyncloop, executor

async def get_youtube_title(url):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, sync_get_youtube_title, url)
    
def sync_get_youtube_title(url):
    if url is not None or "":
        response  = requests.get(url)
        htmlresponse = response.text
        title_match = re.search(r'<title>(.*?) - YouTube</title>', htmlresponse)
        if title_match:
            title = title_match.group(1).strip()
            if title == "":
                print("TITLE IS EMPTY!!!!!!!")
                return "Empty :("
            print(f"returning title {html.unescape(title)}")
            return html.unescape(title)
    
    return "Unknown"

    
def get_metadata_youtube(ctx, url):
    print("getting metadata for youtube")
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict
    
async def get_youtube_link(ctx, search_term):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, sync_get_youtube_link, search_term)
    
def sync_get_youtube_link(search_term):
    print(f"getting youtube link for {search_term}")
    try:
        phrase = urllib.parse.quote(search_term.replace(" ", "+"), safe="+")
        search_link = f"https://www.youtube.com/results?search_query={phrase}"
        response = urllib.request.urlopen(search_link)
        search_results = re.findall(r'watch\?v=(\S{11})', response.read().decode())
        return f"https://www.youtube.com/watch?v={search_results[0]}"
    except Exception as e:
        return None
    
