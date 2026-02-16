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

async def run_download( url: str, quality: int, video: bool):
    
    outputpath = os.path.join("src", "beefcommands", "music_player", "temp")
    cookiefile = os.path.join("src", "beefcommands", "music_player", "cookies.txt")

    python_code = f'''
import sys, json, os, os.path
import yt_dlp

def main():
    src_url = sys.argv[1]
    quality = int(sys.argv[2])
    video = bool(int(sys.argv[3]))
    outputpath = sys.argv[4]
    cookiefile = sys.argv[5]

    ffmpeg_path = os.getenv("FFMPEGEXE")
    js_runtime = os.getenv("JSRUNTIME")

    base_ydl_opts = {{
        "cookiefile": cookiefile if cookiefile and cookiefile != "None" else None,
        "outtmpl": "%(title).200B_%(epoch)s.%(ext)s",
        "restrictfilenames": True,
        "paths": {{"home": outputpath}},
        "enable_ejs": True,
        "js_runtimes": {{
            "deno": {{
                "path": js_runtime,
            }}
        }},
        "remote_components": ["ejs:github"],
        "extractor_args": {{
            "youtube": {{
                "player_client": ["web"]
            }}
        }},
        "ffmpeg_location": ffmpeg_path,
        "ratelimit": 2 * 1024 * 1024,
        "sleep_interval": 2,
        "max_sleep_interval": 6,
        "sleep_interval_requests": 2,
        "concurrent_fragment_downloads": 1,
        "progress_hooks": [],
        "noprogress": True,
        "noplaylist": True,
        "playlist_items": "1",
        "quiet": True
    }}

    audio_opts = {{
        "format": "bestaudio[protocol!=m3u8][protocol!=dash]/bestaudio/best",
        "postprocessors": [{{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }}],
    }}

    video_opts = {{
        "format": (
            f"bestvideo[height<={quality}][ext=mp4]/"
            f"bestvideo[height<={quality}]/"
            f"best[height<={quality}]"
            f"+bestaudio/best"
        ),
        "merge_output_format": "mp4",
    }}

    ydl_opts = dict(base_ydl_opts)
    if video:
        ydl_opts.update(video_opts)
    else:
        ydl_opts.update(audio_opts)

    try:
        os.makedirs(outputpath, exist_ok=True)
    except Exception:
        pass

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(src_url, download=True)
        local_path = ydl.prepare_filename(info)
        if not video:
            base, ext = os.path.splitext(local_path)
            if ext.lower() == ".mp4":
                local_path = base + ".mp3"
        result = {{"title": info.get("title"), "path": local_path}}
        sys.stdout.write(json.dumps(result))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(2)
'''

    try:
        proc = await asyncio.create_subprocess_exec(
            sys.executable, "-c", python_code,
            url, str(quality), "1" if video else "0", outputpath, cookiefile,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()
        stdout_text = stdout.decode().strip()
        stderr_text = stderr.decode().strip()
        
        if proc.returncode != 0:
            return False, stderr_text
    except Exception as e:
            return False, e

    data = json.loads(stdout_text)
    title = data.get("title")
    path = data.get("path")
    return title, path

async def yownload(interaction: discord.Interaction, url: str, quality: int, video: bool):
    channel = interaction.channel
    user = interaction.user

    await resolve_interaction(interaction, url, quality)
    urltype = await validate_inputs(url, quality)
    
    if urltype == "youtube":
        title, path = await run_download(url, quality, video)
    elif urltype == "spotify":
        title, path = await spotify_link_parser(url)

    await write_to_server(path)
    cleanup(path)

    await channel.send(f"{user.mention} Download finished: **{title}**\nPath: {generate_link(path)}")

async def resolve_interaction(interaction: discord.Interaction, url: str, quality: int):
    urltype = await validate_inputs(url, quality)
    
    if urltype != "youtube" and urltype != "spotify":
        await interaction.response.send_message(content=urltype)
        return
    
    await interaction.response.send_message(f"{interaction.user.mention} Download started. I'll post the result here once it's finished.")

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
        return await fetch_playlist(urls, 720, False, album_name)

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
        return await fetch_playlist(urls, 240, False, playlist_name)

    else:
        return None

async def fetch_playlist(src_urls, quality, video, title):
    sem = asyncio.Semaphore(5)

    async def _fetch_with_limit(track):
        async with sem:
            return await run_download(track[0], quality, video)

    urls = await asyncio.gather(*[_fetch_with_limit(t) for t in src_urls])
    return await generate_zip(urls, title)

async def generate_zip(urls, title):
    cleantitle = ''.join([c for c in title if c.isalnum()]) + str(int(time.time()))
    filepath = file_io.construct_root_path(f"src/beefcommands/music_player/temp/{cleantitle}.zip")

    with zipfile.ZipFile(filepath, 'w'):
        pass

    with zipfile.ZipFile(filepath, 'a', compression=zipfile.ZIP_DEFLATED) as zipf:
        for i, track in enumerate(urls, start=1):
            try:
                source_path = track[1]
                destination = f"{i}-{os.path.basename(track[1])}"
                zipf.write(source_path, destination)
                cleanup(track[1])
            except Exception:
                continue
    return title, filepath

async def validate_inputs(url, quality):
    urltype = link_parser.validate_input(url)
    if urltype != "youtube" and urltype != "spotify":
        return "invalid link"
    
    valid_qualitites = [1080, 720, 480, 360, 240]
    
    if not quality in valid_qualitites:
        return "invalid quality format"
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

    smb = SMBConnection(username, password, "local_client", server, use_ntlm_v2=True, is_direct_tcp=True)
    if not smb.connect(server, 445):
        raise RuntimeError("SMB connection failed")
    with open(local_path, "rb") as f:
        smb.storeFile(share, f"{remote_dir}/{remote_name}", f)
    smb.close()

async def write_to_server(local_path):
    print("writing to server")
    await asyncio.to_thread(_write_to_server_sync, local_path)
    print("server write completed")
