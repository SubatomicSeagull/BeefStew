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

# in order to not get tkinter to NOT get the GC to eat the main bot loop we have to run ytdl in a subprocess
# why does ytdl even use tkinter if its a CLI app?????
# anyways this code is shit but i cant really make it any better soz
# does have the benefit that its isolated
async def run_download(url: str, quality: int, video: bool):
    
    outputpath = file_io.construct_root_path("src", "beefcommands", "music_player", "temp")
    cookiefile = file_io.construct_root_path("src", "beefcommands", "music_player", "cookies.txt")
    
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

    print("FFMPEG PATH:", ffmpeg_path, file=sys.stderr)

    if not ffmpeg_path or not os.path.exists(ffmpeg_path):
        print("ERROR: FFmpeg not found or invalid path", file=sys.stderr)
        sys.exit(3)

    base_ydl_opts = {{
        "cookiefile": cookiefile if cookiefile and cookiefile != "None" else None,
        "outtmpl": "%(title).200B_%(epoch)s.%(ext)s",
        "restrictfilenames": True,
        "paths": {{"home": outputpath}},
        "ffmpeg_location": ffmpeg_path,
        "merge_output_format": "mp4",
        "quiet": False,
        "verbose": False,
        "logger": None,
        "progress_with_newline": False,
        "logtostderr": True,
        "noprogress": False,
        "noplaylist": True,
    }}

    audio_opts = {{
        "format": "bestaudio/best",
        "postprocessors": [{{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }}],
    }}

    video_opts = {{
        "format": (
            f"bestvideo[height<={{quality}}]/bestvideo/best"
            f"+bestaudio/best"
        ),
        "merge_output_format": "mp4",
    }}

    ydl_opts = dict(base_ydl_opts)
    ydl_opts.update(video_opts if video else audio_opts)

    os.makedirs(outputpath, exist_ok=True)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(src_url, download=True)
        local_path = ydl.prepare_filename(info)

        if not video and local_path.endswith(".mp4"):
            local_path = os.path.splitext(local_path)[0] + ".mp3"

        sys.stdout.write(json.dumps({{"title": info.get("title"), "path": local_path}}))

if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(2)
'''
    # execution stars here
    proc = await asyncio.create_subprocess_exec(sys.executable, "-u", "-c", python_code,
        url, 
        str(quality), 
        "1" if video else "0", 
        outputpath, 
        cookiefile,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout_lines = []
    # ytdl logs are all output to err coz we need out for the actual output there might be a way around that but i cba atp
    stderr_lines = []

    # reads stderr and prints it to the console so we can see whats going on! probably could turn it off in prod
    async def read_stream(stream, collector):
        while True:
            line = await stream.readline()
            if not line:
                break
            text = line.decode(errors="replace").rstrip()
            collector.append(text)
            print(f"ytdl: {text}")

    await asyncio.gather(read_stream(proc.stdout, stdout_lines, "stdout"), read_stream(proc.stderr, stderr_lines, "stderr"))

    returncode = await proc.wait()

    stdout_text = "\n".join(stdout_lines)
    stderr_text = "\n".join(stderr_lines)

    # TODO currently no way to handle this if it does even happen
    if returncode != 0:
        return False, stderr_text or f"yt-dlp exited with code {returncode}"

    data = json.loads(stdout_text)
    return data["title"], data["path"]


async def yownload(interaction: discord.Interaction, url: str, quality: int, video: bool):
    # grab the user and channel from the interaction to respond to later
    channel = interaction.channel
    user = interaction.user

    # resolve the interaction to allow us to run the logic independently of the webhook
    await resolve_interaction(interaction, url, quality)
    urltype = await validate_inputs(url, quality)
    
    if urltype == "youtube":
        title, path = await run_download(url, quality, video)
    elif urltype == "spotify":
        title, path = await spotify_link_parser(url)
    # more types to come!

    await write_to_server(path)
    cleanup(path)

    await channel.send(f"{user.mention} ding ding!!! ur yownload is finished! click here to get it: [**{title}**]({generate_link(path)})")


async def resolve_interaction(interaction: discord.Interaction, url: str, quality: int):
    urltype = await validate_inputs(url, quality)
    
    if urltype != "youtube" and urltype != "spotify":
        await interaction.response.send_message(content=urltype)
        return
    
    await interaction.response.send_message(f"{interaction.user.mention} on it boss o7 ill lyk when its completed!")

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
    # limit to 5 concurrent steams
    sem = asyncio.Semaphore(5)

    async def _fetch_with_limit(track):
        async with sem:
            return await run_download(track[0], quality, video)

    urls = await asyncio.gather(*[_fetch_with_limit(t) for t in src_urls])
    return await generate_zip(urls, title)

async def generate_zip(urls, title):
    #limit to alphanumeric chars only
    #TODO other language characters will just be blank so mayb open it up a bit
    cleantitle = ''.join([c for c in title if c.isalnum()]) + str(int(time.time()))
    filepath = file_io.construct_root_path(f"src/beefcommands/music_player/temp/{cleantitle}.zip")

    # create empty zip archive
    with zipfile.ZipFile(filepath, 'w'):
        pass

    # populate zip archive with tracks in the array
    with zipfile.ZipFile(filepath, 'a', compression=zipfile.ZIP_DEFLATED) as zipf:
        for i, track in enumerate(urls, start=1):
            try:
                source_path = track[1]
                destination = f"{i}-{os.path.basename(track[1])}"
                zipf.write(source_path, destination)
                # delete them after copying, same as mv operation ig?
                cleanup(track[1])
            except Exception:
                continue
    return title, filepath

async def validate_inputs(url, quality):#
    urltype = link_parser.validate_input(url)
    if urltype != "youtube" and urltype != "spotify":
        return "invalid link"
    
    # no 4k for u
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

    # connect to smb server
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
