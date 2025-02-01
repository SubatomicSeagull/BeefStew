import discord
import random
import os
import re
import yt_dlp
import urllib
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy


queue = []

async def queue_stack(ctx, tracks: list):
    print(f"stacking {tracks} to the front of the queue")
    queue.insert(0, tracks[0])
    
async def queue_push(ctx, tracks: list):
    for track in tracks:
        print(f"pushing {track} to the queue")
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
    
async def queue_list(ctx):
    return queue
    #generate an embed listing the first 10 songs in the queue,
    # is there a way to dynamically add pages?
    
async def queue_embed(ctx):
    pass
#generate a queue embed
# "xyz added abc to the back/front queue"

async def link_validation(url: str):
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

async def media_source(ctx, url: str, type: str):
    links = []
    if type == 'youtube':
        print("youtube link, retrieving metadata")
        links.append(url)
        print(f"links = {links}")
        return links
    elif type == 'spotify':
        print("spotify link, retrieving metadata")
        return links.append(await spotify_link_parser(ctx, url))
    elif type == 'search':
        print("search term, retrieving yt link")        
        return links.append(await yt_link_from_search_term(ctx, url))
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
    print(f"searching youtube for \"{search_term}\"...")
    phrase = search_term.replace(" ", "+")
    search_link = "https://www.youtube.com/results?search_query=" + phrase
    response = urllib.request.urlopen(search_link)
    
    search_results = re.findall(r'watch\?v=(\S{11})', response.read().decode())
    first_result = search_results[0]
    url = "https://www.youtube.com/watch?v=" + first_result
    print(f"first result = {url}")
    return url

async def get_audio_link(ctx, url: str, type: str):
    print(f"putting {url} throught the link parser...")
    metadata = await media_source(ctx, url, type)
    #print(f"metadata = {metadata}")
    return metadata["url"]


sp_client = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv("SPOTIFYCLIENTID"), client_secret=os.getenv("SPOTIFYCLIENTSECRET")))

async def spotify_link_parser(ctx, url: str):
    
    if "track" in url:
        print("single track")  
        return await get_metadata_spotify(ctx, url)
        
    elif "playlist" in url:
        print("playlist")
        playlist = sp_client.playlist(url)
        playlist_tracks = sp_client.playlist_tracks(url)
        playlist_art = sp_client.playlist_cover_image(url)
        count = playlist_tracks['total']
        name = playlist['name']
        
        #all_songs = await playlist_warning(ctx, playlist_art[0]['url'], count, name)
        return await get_metadata_spotify_playlist(ctx, url)
        
        #if all_songs == True:
        #    print("retriving data for all tracks")
        #    return await get_metadata_spotify_playlist(ctx, url)
        #else:
        #    print("retreiving data for first track")
        #    return await get_metadata_spotify_playlist_first_track(ctx, url)
    elif "album" in url:
        print("album")


async def get_metadata_spotify(ctx, url: str):
    track_queries = []
    print("retriving spotify track metadata")
    print("getting track data")
    track = sp_client.track(url)
    print("resolving track name")
    song_name = track["name"]
    print(f"name = {song_name}")
    print("resolving artist name")
    artist = track['artists'][0]['name']
    print(f"artist = {artist}")
    print("constructing search term")
    search_term = str(artist + " - " + song_name)
    print(f"search term = {search_term}")
    yt_link = await yt_link_from_search_term(ctx, search_term)
    print(f"yt link = {yt_link}")

    return track_queries.append(await yt_link_from_search_term(ctx, search_term))
            
async def get_metadata_spotify_playlist(ctx, url: str):
    track_queries = []
    playlist = sp_client.playlist(url)
    print("retrieving spotify playlist metadata")
    song_list = sp_client.playlist_tracks(url)
    tracks = [item["track"] for item in song_list["items"]]
    print(f"iterating tracks in playlist")
    for track in tracks:
        song_name = track["name"]
        artist = track['artists'][0]['name']
        query = (f"{artist} - {song_name}")
        print(f"search term = {query}")
        track_queries.append(await yt_link_from_search_term(ctx, query))
    return track_queries


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