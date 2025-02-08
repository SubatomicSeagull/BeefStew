
import asyncio
from main import executor, asyncloop, sp_client
import math
from beefcommands.utilities.music_player.spotify.playlist_warning import playlistwarning
from beefcommands.utilities.music_player.youtube.youtube_handler import get_youtube_link, get_youtube_title


async def spotify_link_parser(ctx, url):
    loop = asyncio.get_running_loop()
    if "track" in url:
        print("getting metadata for spotify track")

        track = await loop.run_in_executor(executor, sp_client.track, url)
        return [await process_spotify_track(ctx, track)]
    
    if "album" in url:
        album_tracks = await loop.run_in_executor(executor, sp_client.album_tracks, url)
        urls = []
        print("getting metadata for spotify album")
        fetch_album_tracks = await asyncio.gather(*[process_spotify_track(ctx, track)for track in album_tracks["items"]])
        for result in fetch_album_tracks:
            if result is not None:
                urls.append(result)
        return urls
        
    if "playlist" in url:
        playlist = await loop.run_in_executor(executor, sp_client.playlist, url)
        playlist_name = playlist['name']
        playlist_art = playlist['images'][0]['url'] if playlist['images'] else None
        total = playlist['tracks']['total']
        warning_response = await playlistwarning(ctx, playlist_name, playlist_art, total)
        if warning_response is None:
            return []
        
        urls = []
        print("getting metadata for spotify playlist")
        song_list = await loop.run_in_executor(executor, sp_client.playlist_tracks, url)
        total = song_list["total"]
        pages = math.ceil(total / 100)
        
        if warning_response == True:    
            for i in range(pages):
                print(f"fetching page {i}")
                page = sp_client.playlist_tracks(url, offset = i * 100)
                fetch_page = await asyncio.gather(*[process_spotify_track(ctx, item["track"]) for item in page["items"]])
                for result in fetch_page:
                    if result is not None:
                        urls.append(result)
        return urls

    if "artist" in url:
        print("artist link... whajt r u doing")
        return None
    
    
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