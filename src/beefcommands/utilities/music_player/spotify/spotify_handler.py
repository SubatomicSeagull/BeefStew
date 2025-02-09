
import asyncio
from main import executor, sp_client
import math
from beefcommands.utilities.music_player.spotify.playlist_warning import playlistwarning
from beefcommands.utilities.music_player.youtube.youtube_handler import get_youtube_link, get_youtube_title


async def spotify_link_parser(ctx, url):
    # retrive the thread executor pool
    loop = asyncio.get_running_loop()
    
    # https://open.spotify.com/track/...........
    # retrive the metadata of the given spotify track on a different thread
    if "track" in url:
        track = await loop.run_in_executor(executor, sp_client.track, url)
        return [await process_spotify_track(ctx, track)]
    
    # https://open.spotify.com/album/...........
    # retrive the metadata for an album on a different thread and return it to an array
    if "album" in url:
        album_tracks = await loop.run_in_executor(executor, sp_client.album_tracks, url)
        urls = []
        fetch_album_tracks = await asyncio.gather(*[process_spotify_track(ctx, track)for track in album_tracks["items"]])
        for result in fetch_album_tracks:
            if result is not None:
                urls.append(result)
        return urls
    
    #https://open.spotify.com/playlist/...........   
    # retrive the metadata for a playlist on a different thread
    if "playlist" in url:  
        playlist = await loop.run_in_executor(executor, sp_client.playlist, url)
        playlist_name = playlist['name']
        playlist_art = playlist['images'][0]['url'] if playlist['images'] else None
        total = playlist['tracks']['total']
        
        # call the playlist warning
        warning_response = await playlistwarning(ctx, playlist_name, playlist_art, total)
        if warning_response is None:
            return []
        
        # process each track of each page of the playlist in a the thread pool and add it to an array
        urls = []
        
        # retrive the metadata for the playlist track
        song_list = await loop.run_in_executor(executor, sp_client.playlist_tracks, url)
        
        # calculate the number of pages
        total = song_list["total"]
        pages = math.ceil(total / 100)
        
        # if the user wants to add all the songs, process each track for each page
        if warning_response == True:    
            for i in range(pages):
                page = sp_client.playlist_tracks(url, offset = i * 100)
                fetch_page = await asyncio.gather(*[process_spotify_track(ctx, item["track"]) for item in page["items"]])
                for result in fetch_page:
                    if result is not None:
                        urls.append(result)
        return urls
    
    # cant process and artist list
    if "artist" in url:
        ctx.send("artist link... whajt r u doing")
        return None
    
    
async def process_spotify_track(ctx, track):
    # retrive the name and artist
    song_name = track["name"]
    artist = track['artists'][0]['name']
    
    # define a search query "ARTIST - SONG NAME"
    search_term = f"{artist} - {song_name}"
    try:
        # send the query to the youtube link parser
        yt_link = await get_youtube_link(ctx, search_term)
        title = await get_youtube_title(yt_link)
        return (yt_link, title)
    
    # sometimes it cant parse the title
    except Exception as e:
        return None 