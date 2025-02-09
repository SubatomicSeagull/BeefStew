import requests
import re
import html
import yt_dlp
import urllib.request
import urllib.parse
import asyncio
from main import executor

async def get_youtube_title(url):
    # retrive the thread executor loop
    loop = asyncio.get_running_loop()
    
    # retrive the youtube link title in a different thread
    return await loop.run_in_executor(executor, sync_get_youtube_title, url)
    
def sync_get_youtube_title(url):
    if url is not None or "":
        # retrive the html header data from the youtube link as text
        response  = requests.get(url)
        htmlresponse = response.text
        
        # regex pattern to retrive only the title
        title_match = re.search(r'<title>(.*?) - YouTube</title>', htmlresponse)
        if title_match:
            # take out the "- Youtube"
            title = title_match.group(1).strip()
            
            if title == "":
                return "Empty :("
            
            # return the UTF-8 title from the html data
            return html.unescape(title)
    
    return "Unknown"

    
def get_metadata_youtube(ctx, url):
    # define the youtube audio options
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
    }

    # extract the metadata from the youtube video
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict
    
async def get_youtube_link(ctx, search_term):
    # retrive the thread executor loop
    loop = asyncio.get_running_loop()
    
    # generate the youtbe link in a different thread
    return await loop.run_in_executor(executor, sync_get_youtube_link, search_term)
    
def sync_get_youtube_link(search_term):
    try:
        # replace spaces in the query with +
        phrase = urllib.parse.quote(search_term.replace(" ", "+"), safe="+")
        
        # construct the youtube link
        search_link = f"https://www.youtube.com/results?search_query={phrase}"
        
        # retrive the videos given by the link
        response = urllib.request.urlopen(search_link)
        search_results = re.findall(r'watch\?v=(\S{11})', response.read().decode())
        
        # return the first result
        return f"https://www.youtube.com/watch?v={search_results[0]}"
    
    except Exception as e:
        return None
    
