import discord
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from beefcommands.utilities.music_player.spotify.spotify_embed import playlist_warning

sp_client = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv("SPOTIFYCLIENTID"), client_secret=os.getenv("SPOTIFYCLIENTSECRET")))

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
    
