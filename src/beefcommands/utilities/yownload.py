
import os
from smb.SMBConnection import SMBConnection
import asyncio
import yt_dlp
from yt_dlp.utils import DownloadError
from beefutilities.IO import file_io
from beefcommands.music_player import link_parser
from main import bot, sp_client
import math
import zipfile


async def fetch_track(src_url, quality, video):
    ffmpeg_path = os.getenv("FFMPEGEXE")
    
    outputpath = file_io.construct_root_path("src/beefcommands/music_player/temp")
    print(outputpath)
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "%(title).200B_%(epoch)s.%(ext)s",
        "restrictfilenames": True,
        "noplaylist": True,
        "playlist_items": "1",
        "paths": {"home": outputpath},
        "ffmpeg_location": ffmpeg_path,
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]
    }
    
    # if the video flag is set, download at the desired video quality
    if video:
        ydl_opts = {
            "format": f"bestvideo[height={quality}]+bestaudio/best",
            "outtmpl": "%(title).200B_%(epoch)s.%(ext)s",
            "restrictfilenames": True,
            "noplaylist": True,
            "playlist_items": "1",
            "paths": {"home": outputpath},
            "merge_output_format": "mp4",
            "ffmpeg_location": ffmpeg_path,
            "postprocessors": [{
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4"
            }],
            "verbose": True,
        }
        
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(src_url, download=True)
        except DownloadError:
            print(f"No matching format for {quality}p")
            return
        except Exception as e:
            print(f"Error: {e}")
            return
        local_path = ydl.prepare_filename(info)
        
        
        if not video:
            base, ext = os.path.splitext(local_path)
            if ext.lower() == ".mp4":
                local_path = base + ".mp3"
        
        title = info['title']
        
        return title, local_path

def generate_link(path):
    host = os.getenv("HOSTNAME")
    filename = os.path.basename(path)
    return f"https://www.{host}/download/beefstew/{filename}"

async def write_to_server(local_path):
    server = os.getenv("SERVERIP")
    username = os.getenv("SMBUSER")
    password = os.getenv("SMBPASS")

    share = "Share"
    remote_dir = "/download/beefstew"
    remote_name = os.path.basename(str(local_path))

    print(f"connecting to {server}...")
    smb = SMBConnection(username, password, "local_client", server, use_ntlm_v2=True, is_direct_tcp=True)

    if not smb.connect(server, 445):
        raise RuntimeError("SMB connection failed")

    with open(local_path, "rb") as f:
        print(f"writing file {remote_name} to {remote_dir}")
        smb.storeFile(share,f"{remote_dir}/{remote_name}", f)
        print("writefile complete")
    smb.close()
    print("smb connection closed")

async def yownload(url, quality, video):
    link_type = link_parser.validate_input(url)
    
    if link_type == "youtube":
        title, path = await fetch_track(url, quality, video)
        await write_to_server(path)
        return title, generate_link(path)
    
    elif link_type == "spotify":
        title, path = await spotify_link_parser(url)
        await write_to_server(path)
        return title, generate_link(path)
    else:
        return None
    
async def spotify_link_parser(url):
    # retrieve the thread executor pool
    loop = asyncio.get_running_loop()

    # https://open.spotify.com/track/...........
    # retrieve the metadata of the given spotify track on a different thread
    if "track" in url:
        track = await loop.run_in_executor(bot.executor, sp_client.track, url)
        link = await link_parser.process_spotify_track(track)
        return await fetch_track(link[0], 144, False)

    # https://open.spotify.com/album/...........
    # retrieve the metadata for an album on a different thread and return it to an array
    if "album" in url:
        album = await loop.run_in_executor(bot.executor, sp_client.album, url)
        album_name = album['name']
        album_tracks = await loop.run_in_executor(bot.executor, sp_client.album_tracks, url)
        urls = []
        fetch_album_tracks = await asyncio.gather(*[link_parser.process_spotify_track(track)for track in album_tracks["items"]])
        for result in fetch_album_tracks:
            if result is not None:
                urls.append(result)
        return urls, album_name

    #https://open.spotify.com/playlist/...........
    # retrieve the metadata for a playlist on a different thread
    if "playlist" in url:
        playlist = await loop.run_in_executor(bot.executor, sp_client.playlist, url)
        playlist_name = playlist['name']
        total = playlist['tracks']['total']

        # process each track of each page of the playlist in a the thread pool and add it to an array
        urls = []

        # retrieve the metadata for the playlist track
        song_list = await loop.run_in_executor(bot.executor, sp_client.playlist_tracks, url)

        # calculate the number of pages
        total = song_list["total"]
        pages = math.ceil(total / 100)
        
        for i in range(pages):
            print(i)
            page = sp_client.playlist_tracks(url, offset = i * 100)
            fetch_page = await asyncio.gather(*[link_parser.process_spotify_track(item["track"]) for item in page["items"]])
            for result in fetch_page:
                if result is not None:
                    urls.append(result)
        return urls, playlist_name

async def generate_zip(urls, album, quality, video):
    # Open a zip file at the given filepath. If it doesn't exist, create one.
    # If the directory does not exist, it fails with FileNotFoundError
    
    album = ''.join([char for char in album if char.isalnum()])

    # create the empty archive
    archive_name = f'{album}.zip'
    with zipfile.ZipFile(archive_name, 'w') as file:
        pass

    filepath = file_io.construct_root_path("src/beefcommands/music_player/temp/album.zip")
    with zipfile.ZipFile(filepath, "a", compression=zipfile.ZIP_DEFLATED) as zipf:
        # Add a file located at the source_path to the destination within the zip
        
        for track in urls:
            pass
        
        source_path = '/home/user/a/b/c/1.txt'
        destination = 'foobar.txt'
        zipf.write(source_path, destination)