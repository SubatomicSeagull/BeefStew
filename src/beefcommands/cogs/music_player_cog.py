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
import random
import os
from concurrent.futures import ThreadPoolExecutor

class MusicPlayerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @discord.app_commands.command(name="play", description="add")
    async def play(self, interaction: discord.Interaction):
        await interaction.response.send_message("not implemented yet sorry :(")
        
    @discord.app_commands.command(name="play_next", description="play next, skip the queue!")
    async def play_next(self, interaction: discord.Interaction):
        await interaction.response.send_message("not implemented yet sorry :(")
        
    @commands.command(name="queue_add", description="add video to the queue")
    async def queue_add(self, ctx, url: str):
        media_type = link_validation(url)
        print(f"Media type from link_validation: {media_type}")
        
        if media_type != "invalid" and media_type is not None:
            executor.submit(self.process_queue_add, ctx, url, media_type)
            await ctx.send(f"Pushed track(s) to the queue successfully")
        else:
            await ctx.send("Invalid link")

    async def process_queue_add(self, ctx, url: str, media_type: str):
        yt_links = await media_source(ctx, url, media_type)
        for playlist in yt_links:
            for link in playlist:
                response = requests.get, link
                title_match = re.search(r'<title>(.*?) - YouTube</title>', response.text)
                title = title_match.group(1).strip() if title_match else "Unknown Title"
                print(f"Adding [{title}]({link}) to the queue")
                await queue_push(ctx, link)           
        
    @commands.command(name="queue_list", description="list the queue")
    async def queue_list(self, ctx):
        await ctx.send(await asyncio.to_thread(queue_list, ctx))
        
    @discord.app_commands.command(name="skip", description="STREAMER NEXT GAME!!!!!!")
    async def skip(self, interaction: discord.Interaction):
        await interaction.response.send_message("not implemented yet sorry :(")
        
    @discord.app_commands.command(name="pause", description="STOP!!!!!")
    async def stop(self, interaction: discord.Interaction):
        await interaction.response.send_message("not implemented yet sorry :(")
        
    @discord.app_commands.command(name="loop", description="endless nameless...")
    async def loop(self, interaction: discord.Interaction):
        await interaction.response.send_message("not implemented yet sorry :(")
        
    @discord.app_commands.command(name="clear", description="clear the queue")
    async def clear(self, interaction: discord.Interaction):
        await interaction.response.send_message("not implemented yet sorry :(")
        
    @discord.app_commands.command(name="download", description="youtube yownloader")
    async def download(self, interaction: discord.Interaction):
        await interaction.response.send_message("not implemented yet sorry :(")

async def setup(bot):
    print("incantation cog setup")
    await bot.add_cog(MusicPlayerCog(bot))


sp_client = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv("SPOTIFYCLIENTID"), client_secret=os.getenv("SPOTIFYCLIENTSECRET")))
executor = ThreadPoolExecutor(max_workers=1)
queue = []

async def queue_stack(ctx, tracks):
    print(f"stacking {tracks} to the front of the queue")
    queue.insert(0, tracks[0])
    
async def queue_push(ctx, track):
    print("tracks to be pushed: " + track)
    print(f"pushing {track} to the back of the queue") 
    queue.append(track)
    
async def queue_pop(ctx):
    print(f"popping {queue[0]} from the queue")
    queue.pop(0)
    
async def clear(ctx):
    print("clearing the queue")
    queue.clear()
    
async def shuffle(ctx):
    print("shuffling the queue")
    random.shuffle
    
def queue_list(ctx):
    count = 1
    content = ""
    print(f"Queue: {queue}")
    for link in queue:
        print(link)
        response  = requests.get(link)
        title_match = re.search(r'<title>(.*?) - YouTube</title>', response.text)
        if title_match:
            title = title_match.group(1).strip()
        content = content + (f"**{count}.** [{title}]({link})\n")
        count+=1
    print(content)
    return content
    #generate an embed listing the first 10 songs in the queue,
    # is there a way to dynamically add pages?
    
async def queue_embed(ctx):
    pass
#generate a queue embed
# "xyz added abc to the back/front queue"

def link_validation(url: str):
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
    
async def get_metadata_yt(ctx, url: str):
    print("getting yt metadata for " + url)
    
    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True
        }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        print(f"metadata for {url} = {info_dict}")
        return info_dict

async def yt_link_from_search_term(ctx, search_term: str):
    #result = await asyncio.to_thread(yt_link_from_search_term_sync, search_term)
    future = executor.submit(yt_link_from_search_term_sync, search_term)
    result = future.result()
    return result

def yt_link_from_search_term_sync(search_term: str):
    phrase = urllib.parse.quote(search_term.replace(" ", "+"), safe="+")
    search_link = f"https://www.youtube.com/results?search_query={phrase}"
    response = urllib.request.urlopen(search_link)
    search_results = re.findall(r'watch\?v=(\S{11})', response.read().decode())
    print(f"search results for {phrase}: {search_results}")
    return f"https://www.youtube.com/watch?v={search_results[0]}"


async def media_source(ctx, url: str, type: str):
    links = []
    if type == 'youtube':
        links.append([url])
    elif type == 'spotify':
        sp_song = await spotify_link_parser(ctx, url)
        links.append(sp_song)
    elif type == 'search':
        search_song = await yt_link_from_search_term(ctx, url)
        links.append([search_song])
    return links

async def spotify_link_parser(ctx, url: str):
    if "track" in url:
        print("spotify track")
        return await get_metadata_spotify(ctx, url)
    elif "playlist" in url:
        print("spotify playlist")
        return await get_metadata_spotify_playlist(ctx, url)

async def get_metadata_spotify(ctx, url: str):
    print("getting metadata for spotify track")
    track = sp_client.track, url
    song_name = track["name"]
    artist = track['artists'][0]['name']
    search_term = f"{artist} - {song_name}"
    yt_link = await yt_link_from_search_term(ctx, search_term)
    return [yt_link]

async def get_metadata_spotify_playlist(ctx, url: str):
    print("getting metadata for spotify playlist")
    playlist = sp_client.playlist(url)
    song_list = sp_client.playlist_tracks(url)
    tracks = [item["track"] for item in song_list["items"]]
    return [await yt_link_from_search_term(ctx, f"{track['artists'][0]['name']} - {track['name']}") for track in tracks]


async def get_metadata_spotify_playlist_first_track(ctx, url: str):
    pass


#AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

async def playlist_warning(ctx, playlist_art: str, count: int, name: str):  
    view = PlaylistWarningEmbed()
    embed = discord.Embed(title="Spotify Playlist", description="hold on there buddy...", color=discord.Color.green())
    embed.set_thumbnail(url=playlist_art)
    embed.add_field(name=f"{name} has {count} songs.", value= "u wanna add all these?")
    await ctx.response.send_message(embed=embed, view=view)
    
    await view.wait()
    response = view.response

    return response
class PlaylistWarningEmbed(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.response = None
        
    @discord.ui.button(label="all of em babey!!", style=discord.ButtonStyle.primary)
    async def add_all_tracks(self, ctx, button: discord.ui.Button):
        self.response = True
        self.stop()
        await ctx.response.edit_message(content="added all the tracks", embed=None, view=None)
    
    @discord.ui.button(label= "just the one please", style=discord.ButtonStyle.primary)
    async def add_top_track(self, ctx, button: discord.ui.Button):
        self.response = False
        self.stop()
        await ctx.response.edit_message(content="added one track", embed=None, view=None)