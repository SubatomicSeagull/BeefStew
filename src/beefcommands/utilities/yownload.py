import asyncio
import sys
import os
import json
import discord
from main import bot  # ensure your main bot import works here

async def run_download(interaction: discord.Interaction, url: str, quality: int, video: bool):
    # Capture channel before resolving interaction
    channel = interaction.channel

    # Immediately resolve interaction
    await interaction.response.send_message(
        "Download started. I'll post the result here once it's finished."
    )

    # Output path and cookiefile
    outputpath = os.path.join("src", "beefcommands", "music_player", "temp")
    cookiefile = os.path.join("src", "beefcommands", "music_player", "cookies.txt")

    # Build Python snippet for subprocess
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
        "format": f"bestvideo[height={{quality}}]+bestaudio/best",
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

    # Run subprocess
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
        await channel.send(f"Download failed:\n```{stderr_text}```")
        return

    try:
        data = json.loads(stdout_text)
        title = data.get("title")
        path = data.get("path")
        await channel.send(f"Download finished: **{title}**\nPath: `{path}`")
    except Exception:
        await channel.send(f"Download finished but failed to parse output:\n```{stdout_text}```")
