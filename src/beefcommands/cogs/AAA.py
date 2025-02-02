import discord
from discord.ext import commands
import yt_dlp
import requests
import re
import asyncio
import urllib.request
import urllib.parse
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os
from concurrent.futures import ThreadPoolExecutor
import time
import html
import math

queue = []
executor = ThreadPoolExecutor(max_workers=4)
asyncloop = asyncio.get_event_loop()
sp_client = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv("SPOTIFYCLIENTID"), client_secret=os.getenv("SPOTIFYCLIENTSECRET")))

class testCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="qadd", description="list the queue")  
    async def qadd(self, ctx, *args):
        url = " ".join(args)
        #new thread
        media_type = await asyncloop.run_in_executor(executor, validate_input, ctx, url)
        print(f"type from validate_input: {media_type}")
        b4 = time.time()
        if media_type != "invalid" and media_type is not None:
            await ctx.send(f"Queuing songs...")
            ytlinks = await link_parser(ctx, url, media_type)
            print (ytlinks)
            for playlist in ytlinks:
                for link in playlist:
                    queue_push(ctx, link)
            response_time = ((time.time() - b4))
            await ctx.send(f"Pushed to the queue successfully in {round(response_time, 1)} seconds")
        else:
            await ctx.send("Invalid link")
        
            
    @commands.command(name="qlist", description="list the queue")
    async def qlist(self, ctx):
        for i in range(len(queue)):
            print(queue[i])
        count = 1
        content = ""
        content = content + (f"Queue:\n")
        for link in queue:
            if count < 11:
                content = content + (f"**{count}.** {link[1]}\n")
            count+=1
        print(content)
        if count > 11:
            await ctx.send(f"{content}...\n and {count - 10} other tracks.")
        else:
            await ctx.send(content)

async def setup(bot):
    print("incantation cog setup")
    await bot.add_cog(testCog(bot))
    
async def get_youtube_title(url):
    return await asyncloop.run_in_executor(executor, sync_get_youtube_title, url)
    
def sync_get_youtube_title(url):
    response  = requests.get(url)
    htmlresponse = response.text
    title_match = re.search(r'<title>(.*?) - YouTube</title>', htmlresponse)
    if title_match:
        title = title_match.group(1).strip()
        if title == "":
            print("TITLE IS EMPTY!!!!!!!")
            return "Empty :(`"
        print(f"returning title {html.unescape(title)}")
        return html.unescape(title)
    else:
        return "Unknown"

def queue_push(ctx, track):
    print(f"pushing {track} to the back of the queue") 
    queue.append(track)

def validate_input(ctx, url):
    print("validating the link")
    youtube_pattern = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+')
    spotify_pattern = re.compile(r'(https?://)?(open\.)?spotify\.com/.+')
    search_pattern = re.compile(r'^(?!https?://).+')

    if youtube_pattern.match(url):
        return "youtube"
    elif spotify_pattern.match(url):
        return "spotify"
    elif search_pattern.match(url):
        return "search"
    else:
        return "invalid"
    
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
    #new thread
    return await asyncloop.run_in_executor(executor, sync_get_youtube_link, search_term)
    
def sync_get_youtube_link(search_term):
    print(f"getting youtube link for {search_term}")
    phrase = urllib.parse.quote(search_term.replace(" ", "+"), safe="+")
    search_link = f"https://www.youtube.com/results?search_query={phrase}"
    response = urllib.request.urlopen(search_link)
    search_results = re.findall(r'watch\?v=(\S{11})', response.read().decode())
    return f"https://www.youtube.com/watch?v={search_results[0]}"
    
async def link_parser(ctx, url, type):
    return_links = []
    if type == 'youtube':
        title = await get_youtube_title(url)
        return_links.append([(url, title)])
    elif type == 'spotify':
        sp_song = await spotify_link_parser(ctx, url)
        return_links.append(sp_song)
    elif type == 'search':
        search_song = await get_youtube_link(ctx, url)
        title = await get_youtube_title(search_song)
        return_links.append([(search_song, title)])
    return return_links

async def spotify_link_parser(ctx, url):
    if "track" in url:
        print("getting metadata for spotify track")

        track = await asyncloop.run_in_executor(executor, sp_client.track, url)
        return await process_spotify_track(ctx, track)
    
    if "album" in url:
        pass
    
    if "playlist" in url:
        urls = []
        print("getting metadata for spotify playlist")
        song_list = await asyncloop.run_in_executor(executor, sp_client.playlist_tracks, url)
        total = song_list["total"]
        pages = math.ceil(total / 100)
        #playlist_tracks = [item["track"] for item in song_list["items"]]
        #for track in playlist_tracks:
        #   item = await process_spotify_track(ctx, track)
        #    urls.append(item)
        
        for i in range(pages):
            print(f"fetching page {i}")
            page = sp_client.playlist_tracks(url, offset = i * 100)
            fetch_page = await asyncio.gather(*[process_spotify_track(ctx, item["track"]) for item in page["items"]])
            for result in fetch_page:
                if result is not None:
                    urls.append(result)
            print(f"count: {len(urls)}")
        return urls

async def process_spotify_track(ctx, track):
    song_name = track["name"]
    artist = track['artists'][0]['name']
    search_term = f"{artist} - {song_name}"
    try:
        yt_link = await get_youtube_link(ctx, search_term)
        title = await get_youtube_title(yt_link)
        return (yt_link, title)
    except Exception as e:
        print(f"\n \n ==========================failed to process track {song_name}, skipping. ({e})==================== \n \n )")
        return None
    


class PlaylistWarningEmbed(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.response = None
        
    @discord.ui.button(label="all of em babey!!", style=discord.ButtonStyle.primary)
    async def add_all_tracks(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.response = True
        self.stop()
        await self.ctx.send(content="added all the tracks", embed=None, view=None)
    
    @discord.ui.button(label= "just the one please", style=discord.ButtonStyle.primary)
    async def add_top_track(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.response = False
        self.stop()
        await self.ctx.send(content="added one track", embed=None, view=None)
        
async def playlistwarning(ctx, playlist_name, playlist_art, count):
    warning_embed = discord.Embed(title=playlist_name, description="hold on there buddy...", color=discord.Color.green())
    warning_embed.set_thumbnail(url=playlist_art)
    warning_embed.add_field(name="", value=f"{playlist_name}, has {count} songs, do you want to add them all?")
    
    view = PlaylistWarningEmbed(ctx)
    await ctx.send(embed=warning_embed, view=view)
    
    await view.wait()
    return view.response