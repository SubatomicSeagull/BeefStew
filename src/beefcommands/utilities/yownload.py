import os
import sys
import json
import asyncio
import math
import zipfile
import discord
import time
from smb.SMBConnection import SMBConnection
from beefutilities.IO import file_io
from beefcommands.music_player import link_parser
from main import bot, sp_client
import re
import unicodedata

# in order to not get tkinter to NOT get the GC to eat the main bot loop we have to run ytdl in a subprocess
# why does ytdl even use tkinter if its a CLI app?????
# anyways this code is shit but i cant really make it any better soz
# does have the benefit that its isolated
async def run_download(url: str, quality: int, video: bool):
    outputpath = file_io.construct_root_path("src", "beefcommands", "music_player", "temp")
    cookiefile = file_io.construct_root_path("src", "beefcommands", "music_player", "cookies.txt")

    print(f"attempting to download video at {str(quality)} with video: {str(video)} from {url}")
    
    python_code = r'''
import sys, json, os, os.path
import yt_dlp

def main():
    src_url = sys.argv[1]
    quality = int(sys.argv[2])
    video = bool(int(sys.argv[3]))
    outputpath = sys.argv[4]
    cookiefile = sys.argv[5]

    ffmpeg_path = os.getenv("FFMPEGEXE")

    if not ffmpeg_path or not os.path.exists(ffmpeg_path):
        sys.stdout.write(json.dumps({
            "ok": False,
            "error": "FFmpeg not found or invalid path"
        }, ensure_ascii=False))
        sys.exit(1)

    base_ydl_opts = {
        "cookiefile": cookiefile if cookiefile and cookiefile != "None" else None,
        "outtmpl": "%(title).200B.%(ext)s",
        "restrictfilenames": True,
        "paths": {"home": outputpath},
        "ffmpeg_location": ffmpeg_path,
        "merge_output_format": "mp4",
        "logtostderr": True,
        "noplaylist": True,
    }

    audio_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    video_opts = {
        "format": (
            f"bestvideo[height<={quality}]/bestvideo/best"
            f"+bestaudio/best"
        ),
        "merge_output_format": "mp4",
    }

    ydl_opts = dict(base_ydl_opts)
    ydl_opts.update(video_opts if video else audio_opts)

    os.makedirs(outputpath, exist_ok=True)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(src_url, download=True)
            local_path = ydl.prepare_filename(info)

            if not video:
                local_path = os.path.splitext(local_path)[0] + ".mp3"

            sys.stdout.write(json.dumps({
                "ok": True,
                "title": info.get("title"),
                "path": local_path
            }, ensure_ascii=False))

    except Exception as e:
        sys.stdout.write(json.dumps({
            "ok": False,
            "error": str(e)
        }, ensure_ascii=False))
        sys.exit(1)

if __name__ == "__main__":
    main()
'''

    print("starting the downloader subprocess")
    proc = await asyncio.create_subprocess_exec(
        sys.executable, "-u", "-c", 
        python_code,
        url,
        str(quality),
        "1" if video else "0",
        outputpath,
        cookiefile,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()
    stdout_text = stdout.decode(errors="replace").strip()
    stderr_text = stderr.decode(errors="replace").strip()

    if not stdout_text:
        return False, stderr_text # or "yt-dlp failed without output"

    try:
        data = json.loads(stdout_text)
    except json.JSONDecodeError:
        return False, "Invalid response from yt-dlp subprocess"

    print("donwload completed.")
    
    path = data["path"]
    title = os.path.basename(path)

    
    print("outputs from the downloader:")
    print(f"title: {title}")
    print(f"path: {path}")
    
    return True, title, path

async def yownload(interaction: discord.Interaction, url: str, quality: int, video: bool):
    # grab the user and channel from the interaction to respond to later
    channel = interaction.channel
    user = interaction.user

    # resolve the interaction to allow us to run the logic independently of the webhook
    print("resolving interaciton")
    urltype = await resolve_interaction(interaction, url, quality)
    
    # stop if nothing to yownload
    if not urltype:
        return
    
    try:
        if urltype == "youtube":
            print("running youtube downloader")
            status, *result = await run_download(url, quality, video)
        elif urltype == "spotify":
            print("running spotify downloader")
            status, *result = await spotify_link_parser(url)
        else:
            return
        # more types to come!

        # catch errors in ytdl subprocess
        if not status:
            error = result[0]
            await channel.send(f"{user.mention} ghuhhh i bungled it sorryyy :\n```{error}```")
            return
        print("process ended with status: " + str(status))
        print(result)
        title, path = result
        
        print("title:" + title)
        print("path: " + path)

        await write_to_server(path)
        cleanup(path)

        await channel.send(f"{user.mention} ding ding!!! ur yownload is finished! click here to get it: [**{title}**]({generate_link(path)})")
        return
    
    # catch errors in anything else like spotipy
    except Exception as e:
        await channel.send(
            f"{user.mention} ghhh something broke hard D: \n```{e}```"
        )

async def resolve_interaction(interaction: discord.Interaction, url: str, quality: int):
    print("validating input")
    urltype = await validate_inputs(url, quality)
    
    if urltype != "youtube" and urltype != "spotify":
        await interaction.response.send_message(content=urltype)
        return False
    print(f"received valid input of: {urltype}")

    await interaction.response.send_message(f"{interaction.user.mention} on it boss o7 ill lyk when its completed!")
    print("interaciton resolved")
    return urltype

# p much the same code as in the music player sorryyyyyyy
async def spotify_link_parser(url):
    loop = asyncio.get_running_loop()

    if "track" in url:
        track = await loop.run_in_executor(bot.executor, sp_client.track, url)
        link = await link_parser.process_spotify_track(track)
        return await run_download(link[0], 240, False)

    elif "album" in url:
        album = await loop.run_in_executor(bot.executor, sp_client.album, url)
        album_name = album['name']
        album_tracks = await loop.run_in_executor(bot.executor, sp_client.album_tracks, url)

        urls = []
        processed = await asyncio.gather(*[link_parser.process_spotify_track(t) for t in album_tracks["items"]])
        urls.extend([x for x in processed if x])
        title, path = await fetch_playlist(urls, 240, False, album_name)
        print("from fetchalbum")
        print(title)
        print(path)
        return "ok", title, path 

    elif "playlist" in url:
        playlist = await loop.run_in_executor(bot.executor, sp_client.playlist, url)
        playlist_name = playlist['name']
        total = playlist['tracks']['total']
        pages = math.ceil(total / 100)

        urls = []
        for i in range(pages):
            page = await loop.run_in_executor(bot.executor, lambda: sp_client.playlist_tracks(url, offset=i*100))
            processed = await asyncio.gather(*[link_parser.process_spotify_track(item["track"]) for item in page["items"]])
            urls.extend([x for x in processed if x])
        title, path = await fetch_playlist(urls, 240, False, playlist_name)
        print("from fetchplaylist")
        print(title)
        print(path)
        return "ok", title, path 

    else:
        return None

async def fetch_playlist(src_urls, quality, video, title):
    # limit to 5 concurrent steams
    sem = asyncio.Semaphore(5)

    async def _fetch_with_limit(track):
        async with sem:
            return await run_download(track[0], quality, video)

    urls = await asyncio.gather(*[_fetch_with_limit(t) for t in src_urls])
    return await generate_zip(urls, title)

def clean_title(title):
    print("sanitising title: " + title)
    # normalize unicode
    title = unicodedata.normalize("NFKC", title)

    # split and store the extension if there is one
    name, ext = os.path.splitext(title)

    # remove ASCII control characters
    name = name.translate({i: None for i in range(32)})

    # remove windows invalid chars
    name = re.sub(r'[<>:"/\\|?*]', '_', name)

    # remove other punctiation
    name = re.sub(r'[^\w\s.\-]', '', name, flags=re.UNICODE)

    # replace spaces with underscores
    name = re.sub(r'\s+', '_', name).strip('._')

    print(f"sanitised name: {name}{ext}")
    return f"{name}{ext}" if ext else name


async def generate_zip(urls, title):
    
    cleantitle = clean_title(title)
    
    filepath = file_io.construct_root_path(f"src/beefcommands/music_player/temp/{cleantitle}.zip")

    # create empty zip archive
    with zipfile.ZipFile(filepath, 'w'):
        pass

    # populate zip archive with tracks in the array
    with zipfile.ZipFile(filepath, 'a', compression=zipfile.ZIP_DEFLATED) as zipf:
        for i, track in enumerate(urls, start=1):
            try:
                source_path = track[2]
                destination = f"{i}-{clean_title(os.path.basename(track[2]))}"
                zipf.write(source_path, destination)
                # delete them after copying, same as mv operation ig?
                cleanup(track[2])
            except Exception:
                continue
    print("fromzip")
    print(title)
    print(filepath)
    return title, filepath

async def validate_inputs(url, quality):
    urltype = link_parser.validate_input(url)
    if urltype != "youtube" and urltype != "spotify":
        return "paste a valid link plzzz"
    
    # no 4k for u
    valid_qualitites = [1080, 720, 480, 360, 240]
    
    if not quality in valid_qualitites:
        return "idk how u managed it but u broke the quality format can u be more normal when running commands plz"
    return urltype

def cleanup(path):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        print(f"cleanup failed for {path}: {e}")

def generate_link(path):
    print("generating link")
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
    remote_name = os.path.basename(local_path)

    # connect to smb server
    smb = SMBConnection(username, password, "local_client", server, use_ntlm_v2=True, is_direct_tcp=True)
    if not smb.connect(server, 445):
        raise RuntimeError("SMB connection failed")
    
    with open(local_path, "rb") as f:
        print(f"writing to server from localpath: {local_path}\nwriting: {remote_name} to {remote_dir}")
        smb.storeFile(share, f"{remote_dir}/{remote_name}", f)
    smb.close()

async def write_to_server(local_path):
    print("writing to server")
    await asyncio.to_thread(_write_to_server_sync, local_path)
    print("server write completed")
