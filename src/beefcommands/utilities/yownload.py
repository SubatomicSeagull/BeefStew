""""
reruse code from the media player to generate a link to yt media to download it
spotify (& soundcloud?) can get queried to yt

takes in two arguments the url and audio or audio/video flag
audio flag will just return the audio, audio/video will return the whole video
maybe quality settings but idk yet

find a way to shorten the link, using the embed links thing so (message)<url> i dont remember the syntax
maybe support for playlists?
if so then all this needs to be multithreaded so that it doesnt tank when ppl are downloading stuff,
also how do we collate playlist links into one file?

"""

import discord
import beefcommands.music_player.link_parser as parser
import asyncio
import yt_dlp

async def yownload(interaction: discord.Interaction, src_url, AV, quality):
    
    url = ""
    
    
    
    return url