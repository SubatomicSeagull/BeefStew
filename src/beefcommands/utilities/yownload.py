import os
import sys
import json
import asyncio
import math
import zipfile
import discord
import time
import threading
from smb.SMBConnection import SMBConnection
from yt_dlp.utils import DownloadError
from beefutilities.IO import file_io
from beefcommands.music_player import link_parser
from main import bot, sp_client
import queue
import traceback

# -------------------------
# Thread-safe download queue
# -------------------------
download_queue = queue.Queue()
_worker_started = False
_worker_lock = threading.Lock()


def ensure_worker_running():
    global _worker_started

    if _worker_started:
        print("worker process is started")
        return

    with _worker_lock:
        if _worker_started:
            print("worker process is started")
            return

        print("worker process is not started, starting...")
        loop = asyncio.new_event_loop()
        t = threading.Thread(
            target=download_worker,
            args=(loop,),
            daemon=True,
            name="yt-dlp-subprocess-worker"
        )
        t.start()
        _worker_started = True


def download_worker(loop: asyncio.AbstractEventLoop):
    asyncio.set_event_loop(loop)
    print("download worker started")
    loop.run_until_complete(worker_loop())


async def worker_loop():
    while True:
        # Block on queue.get() without blocking event loop
        job = await asyncio.get_running_loop().run_in_executor(
            None,
            download_queue.get
        )

        url, quality, video, channel, user = job

        try:
            print("fetching source")
            title, path = await fetch_source(url, quality, video)

            print("writing to server")
            await write_to_server(path)

            print("generating link")
            link = generate_link(path)

            print("sending user notification")

            # Schedule Discord API call on main bot loop
            asyncio.run_coroutine_threadsafe(
                notify_user(channel, user, title, link),
                bot.loop
            )

        except Exception as e:
            print("[download error]")
            traceback.print_exc()

            asyncio.run_coroutine_threadsafe(
                channel.send(f"{user.mention} download failed: `{e}`"),
                bot.loop
            )

        finally:
            download_queue.task_done()


# -------------------------
# Fetch source (yt-dlp subprocess)
# -------------------------
async def fetch_source(src_url, quality, video):
    ffmpeg_path = os.getenv("FFMPEGEXE")
    outputpath = file_io.construct_root_path("src/beefcommands/music_player/temp")
    cookies = file_io.construct_root_path("cookies.txt")

    try:
        print("starting yt-dlp subrocess")
        return await _fetch_source_subprocess(src_url, quality, bool(video), outputpath, cookies, ffmpeg_path)
    except DownloadError:
        raise
    except Exception as e:
        print(f"Error in fetch_source: {e}")
        raise


async def _fetch_source_subprocess(src_url, quality, video, outputpath, cookiefile, ffmpeg_path):
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
    js_runtime = os.getenv("JSRUNTIME")

    base_ydl_opts = {
        "cookiefile": cookiefile if cookiefile and cookiefile != "None" else None,
        "outtmpl": "%(title).200B_%(epoch)s.%(ext)s",
        "restrictfilenames": True,
        "paths": {"home": outputpath},
        "enable_ejs": True,
        "js_runtimes": {
            "deno": {
                "path": js_runtime,
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
        result = {"title": info.get("title"), "path": local_path}
        sys.stdout.write(json.dumps(result))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(2)
'''
    python_exe = sys.executable or "python"
    args = [python_exe, "-u", "-c", python_code, src_url, str(quality), "1" if video else "0", outputpath, cookiefile]

    env = os.environ.copy()
    if ffmpeg_path: env["FFMPEGEXE"] = ffmpeg_path

    proc = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env
    )

    stdout, stderr = await proc.communicate()
    stdout_text = stdout.decode().strip()
    stderr_text = stderr.decode().strip()

    if proc.returncode != 0:
        raise RuntimeError(f"yt-dlp subprocess failed (returncode={proc.returncode}). Stderr: {stderr_text}")

    if not stdout_text:
        raise RuntimeError(f"yt-dlp subprocess returned no output. Stderr: {stderr_text}")

    try:
        data = json.loads(stdout_text)
    except Exception as e:
        raise RuntimeError(f"Failed to parse output: {e}. stdout: {stdout_text} stderr: {stderr_text}")

    if "title" not in data or "path" not in data:
        raise RuntimeError(f"Incomplete data from yt-dlp subprocess: {data}")

    print("ytdl python subprocess finished executing")
    return data["title"], data["path"]


# -------------------------
# Spotify handling
# -------------------------
async def spotify_link_parser(url):
    loop = asyncio.get_running_loop()

    if "track" in url:
        track = await loop.run_in_executor(bot.executor, sp_client.track, url)
        link = await link_parser.process_spotify_track(track)
        return await fetch_source(link[0], 240, False)

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
        return await fetch_playlist(urls, 720, False, playlist_name)

    else:
        return None


# -------------------------
# Fetch playlist
# -------------------------
async def fetch_playlist(src_urls, quality, video, title):
    sem = asyncio.Semaphore(5)

    async def _fetch_with_limit(track):
        async with sem:
            return await fetch_source(track[0], quality, video)

    urls = await asyncio.gather(*[_fetch_with_limit(t) for t in src_urls])
    return await generate_zip(urls, title)


# -------------------------
# Zip helper
# -------------------------
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


# -------------------------
# Utility functions
# -------------------------
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


# -------------------------
# Discord interaction
# -------------------------
async def handle_download(interaction: discord.Interaction, url, quality, video):
    ensure_worker_running()
    channel = interaction.channel
    user = interaction.user

    await interaction.response.send_message(
        "On it — I'll ping you when the download is ready.", ephemeral=True
    )

    # enqueue the job synchronously
    download_queue.put((url, quality, video, channel, user))


async def notify_user(channel: discord.TextChannel, user: discord.Member, title, link):
    await channel.send(f"{user.mention} ding!! all done fetching **{title}**\nclick [HERE]({link}) to yownload!")
