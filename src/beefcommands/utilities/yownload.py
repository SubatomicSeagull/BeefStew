
import os
from smb.SMBConnection import SMBConnection
import asyncio
import yt_dlp
from yt_dlp.utils import DownloadError
from beefutilities.IO import file_io


def yownload(src_url, quality, video):
    ffmpeg_path = os.getenv("FFMPEGEXE")
    
    outputpath = file_io.construct_root_path("src/beefcommands/music_player/temp")
    print(outputpath)
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "%(title).200B_%(epoch)s.%(ext)s",
        "restrictfilenames": True,
        "noplaylist": True,
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
            
        write_to_server(local_path)
        
        print("removing local copy")
        os.remove(local_path)
        
        title = info['title']
        
        return title, generate_link(os.path.basename(str(local_path)))

def generate_link(filename):
    host = os.getenv("HOSTNAME")
    return f"https://www.{host}/download/beefstew/{filename}"

def write_to_server(local_path):
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