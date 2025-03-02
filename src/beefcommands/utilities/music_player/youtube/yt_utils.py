import yt_dlp
import discord

async def find_newest_yt_video(channel):
    ydl_opts = {
        'skip_download': True,
        'quiet': True,
        'extract_flat': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel, download=False)

    # 'entries' is a list of video entries; the first is the most recent
    if info.get("entries"):
        name= info["channel"]
        latest_video = info["entries"][0]
        url = latest_video.get("id")
        title = latest_video.get("title")
        return name, url, title
    else:
        print("No videos found.")  
        return None, None