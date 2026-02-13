
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
import discord
import time

async def fetch_source(src_url, quality, video):
    print("fetching from source")
    try:
        return await asyncio.to_thread(_fetch_source_sync, src_url, quality, video)
    except DownloadError:
        print(f"No matching format for {quality}p")
    except Exception as e:
        print(f"Error: {e}")

def _fetch_source_sync(src_url, quality, video):
    ffmpeg_path = os.getenv("FFMPEGEXE")
    outputpath = file_io.construct_root_path("src/beefcommands/music_player/temp")
    cookies = file_io.construct_root_path("cookies.txt")
    
    base_ydl_opts = {
        "cookiefile": cookies,
        "outtmpl": "%(title).200B_%(epoch)s.%(ext)s",
        "restrictfilenames": True,
        "paths": {"home": outputpath},
        "enable_ejs": True,
        "js_runtimes": {
            "deno": {
                "path": os.getenv("JSRUNTIME"),
            }
        },
        "remote_components": ["ejs:github"],
        "extractor_args": {
            "youtube": {
                "player_client": ["web"]
            }
        },
        "ffmpeg_location": ffmpeg_path,
        "ratelimit": 2 * 1024 * 1024,
        "sleep_interval": 2,
        "max_sleep_interval": 6,
        "sleep_interval_requests": 2,
        "concurrent_fragment_downloads": 1,
        "progress_hooks": [],
        "noprogress": True,
        "quiet": True
    }
    
    audio_opts = {
        "format": "bestaudio[protocol!=m3u8][protocol!=dash]/bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }
    
    video_opts = {
        "format": f"bestvideo[height={quality}]+bestaudio/best",
        "merge_output_format": "mp4",
    }
    
    ydl_opts = dict(base_ydl_opts)

    if video:
        ydl_opts.update(video_opts)
    else:
        ydl_opts.update(audio_opts)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print("extracting info")
        info = ydl.extract_info(src_url, download=True)
        print("preparing filename")
        local_path = ydl.prepare_filename(info)

        if not video:
            base, ext = os.path.splitext(local_path)
            if ext.lower() == ".mp4":
                local_path = base + ".mp3"
        print(f"returning info {info}")
        return info["title"], local_path

def generate_link(path):
    host = os.getenv("HOSTNAME")
    filename = os.path.basename(path)
    cleanup(path)
    return f"https://www.{host}/download/beefstew/{filename}"

def _write_to_server_sync(local_path):
    server = os.getenv("SERVERIP")
    username = os.getenv("SMBUSER")
    password = os.getenv("SMBPASS")

    share = "Share"
    remote_dir = "/download/beefstew"
    remote_name = os.path.basename(str(local_path))

    smb = SMBConnection(username, password, "local_client", server, use_ntlm_v2=True, is_direct_tcp=True)

    if not smb.connect(server, 445):
        raise RuntimeError("SMB connection failed")

    with open(local_path, "rb") as f:
        smb.storeFile(share, f"{remote_dir}/{remote_name}", f)
    smb.close()

async def write_to_server(local_path):
    await asyncio.to_thread(_write_to_server_sync, local_path)

async def yownload(url, quality, video):
    link_type = link_parser.validate_input(url)
    
    if link_type == "youtube":
        title, path = await fetch_source(url, quality, video)
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
        return await fetch_source(link[0], 240, False)

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
        return await fetch_playlist(urls, 720, False, album_name)

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
            page = await loop.run_in_executor(bot.executor, lambda: sp_client.playlist_tracks(url, offset=i * 100))
            fetch_page = await asyncio.gather(*[link_parser.process_spotify_track(item["track"]) for item in page["items"]])
            for result in fetch_page:
                if result is not None:
                    urls.append(result)
        return await fetch_playlist(urls, 720, False, playlist_name)
    else:
        return None

async def fetch_playlist(src_urls, quality, video, title):
    
    urls = []
    
    # fetch the source of the youtube links distributed across multiple threads
    sem = asyncio.Semaphore(5)
    async def _fetch_with_limit(track):
        async with sem:
            return await fetch_source(track[0], quality, video)

    urls = await asyncio.gather(*[_fetch_with_limit(t) for t in src_urls])
        
    print(urls)
    
    return await generate_zip(urls, title)

def cleanup(path):
    os.remove(path)

async def generate_zip(urls, title):
    # Open a zip file at the given filepath. If it doesn't exist, create one.
    # If the directory does not exist, it fails with FileNotFoundError
    
    cleantitle = ''.join([char for char in title if char.isalnum()]) + str(int(time.time()))

    # create the empty archive
    filepath = file_io.construct_root_path(f"src/beefcommands/music_player/temp/{cleantitle}.zip")
    print(f"creating zip file {cleantitle}.zip")
    with zipfile.ZipFile(filepath, 'w') as file:
        pass

    print("opening zip archive")
    with zipfile.ZipFile(filepath, "a", compression=zipfile.ZIP_DEFLATED) as zipf:
        # Add a file located at the source_path to the destination within the zip
        index = 0
        for track in urls:
            index +=1
            try:
                source_path = track[1]
            except Exception as e:
                continue
            destination = (str(index) + "-" + os.path.basename(track[1]))
            zipf.write(source_path, destination)
            print(f"wrote {track[0]} to the zip archive from {track[1]}")
            cleanup(track[1])
    return title, filepath

async def handle_download(interaction: discord.Interaction, url, quality, video):
    
    channel = interaction.channel
    user = interaction.user
    
    await interaction.response.send_message("on it boss o7 this will take a while so ill notify u when ur yownload is ready!", ephemeral=True)
    title, link = await yownload(url, quality, video)
    await notify_user(channel, user, title, link)

async def notify_user(channel: discord.TextChannel, user: discord.Member, title, link):
    await channel.send(f"{user.mention} ding!! all done fetching **{title}**\nclick [HERE]({link}) to yownload!")
