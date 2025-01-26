import os
import re
import yt_dlp
import urllib.request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import discord
from discord.ext import commands

sp_client = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv("SPOTIFYCLIENTID"), client_secret=os.getenv("SPOTIFYCLIENTSECRET")))

async def link_validation(url: str):
    print("validating the link")
    youtube_pattern = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+')
    spotify_pattern = re.compile(r'(https?://)?(open\.)?spotify\.com/.+')
    search_pattern = re.compile(r'^(?!https?://).+')

    if youtube_pattern.match(url):
        return True, "youtube"
    elif spotify_pattern.match(url):
        return True, "spotify"
    elif search_pattern.match(url):
        return True, "search"
    else:
        return False, "invalid"

async def link_parser(interaction: discord.Interaction, url: str):
    (valid, type) = await link_validation(url)
    
    if type == 'youtube':
        print("youtube link, retrieving metadata")
        return await get_metadata_yt(interaction, url)
    elif type == 'spotify':
        print("spotify link, retrieving metadata")
        return await spotify_link_parser(interaction, url)
    elif type == 'search':
        print("search term, retrieving yt link")        
        return await yt_search(interaction, url)

async def get_metadata_yt(interaction: discord.Interaction, url: str):
    print("getting yt metadata")
    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict


async def spotify_link_parser(interaction: discord.Interaction, url: str):
    if "track" in url:  
        await get_metadata_spotify(url)
    
    elif "playlist" in url:
        
        playlist = sp_client.playlist(url)
        playlist_tracks = sp_client.playlist_tracks(url)
        playlist_art = sp_client.playlist_cover_image(url)
        count = playlist_tracks['total']
        name = playlist['name']
        
        all_songs = await playlist_warning(interaction, playlist_art[0]['url'], count, name)
        
        if all_songs == True:
            print("retriving data for all tracks")
            return await get_metadata_spotify_playlist(url)
        else:
            print("retreiving data for first track")
            return await get_metadata_spotify_playlist_first_track(url)

async def get_metadata_spotify(interaction: discord.Interaction, url: str):
    print("retriving spotify track metadata")
    
    track = sp_client.track(url)
    song_name = track["name"]
    artist = track['artists'][0]['name']
    
    yt_search_term = (f"{artist} - {song_name}")
    return yt_search_term
            
async def get_metadata_spotify_playlist(url: str):
    song_list = sp_client.playlist_tracks(url)
    
    tracks = [item["track"] for item in song_list["items"]]
    track_queries = []
    for track in tracks:
        song_name = track["name"]
        artist = track['artists'][0]['name']
        query = (f"{artist} - {song_name}")
        track_queries.append(query)
    print(track_queries)


async def get_metadata_spotify_playlist_first_track(interaction: discord.Interaction, url: str):
    pass
#gets the first trackl of the playlist
    
async def playlist_warning(interaction: discord.Interaction, playlist_art: str, count: int, name: str):  
    view = PlaylistWarningEmbed()
    embed = discord.Embed(title="Spotify Playlist", description="hold on there buddy...", color=discord.Color.green())
    embed.set_thumbnail(url=playlist_art)
    embed.add_field(name=f"{name} has {count} songs.", value= "u wanna add all these?")
    await interaction.response.send_message(embed=embed, view=view)
    
    await view.wait()
    response = view.response

    return response
class PlaylistWarningEmbed(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.response = None
        
    @discord.ui.button(label="all of em babey!!", style=discord.ButtonStyle.primary)
    async def add_all_tracks(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.response = True
        self.stop()
        await interaction.response.edit_message(content="added all the tracks", embed=None, view=None)
    
    @discord.ui.button(label= "just the one please", style=discord.ButtonStyle.primary)
    async def add_top_track(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.response = False
        self.stop()
        await interaction.response.edit_message(content="added one track", embed=None, view=None)
    
async def yt_search(interaction: discord.Interaction, search_term: str):
    print(f"searching youtube for \"{search_term}\"...")
    phrase = search_term.replace(" ", "+")
    search_link = "https://www.youtube.com/results?search_query=" + phrase
    response = urllib.request.urlopen(search_link)
    
    search_results = re.findall(r'watch\?v=(\S{11})', response.read().decode())
    first_result = search_results[0]
    url = "https://www.youtube.com/watch?v=" + first_result
    return await get_metadata_yt(interaction, url)

async def get_audio_link(interaction: discord.Interaction, url: str):
    print(f"putting {url} throught the link parser...")
    metadata = await link_parser(interaction, url)
    return metadata["url"]