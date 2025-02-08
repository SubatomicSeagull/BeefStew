import discord
from discord.ext import commands
import yt_dlp
import requests
import re
import asyncio
import urllib.request
import urllib.parse
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os
from concurrent.futures import ThreadPoolExecutor
import html
import math
import random


executor = ThreadPoolExecutor(max_workers=4)
asyncloop = asyncio.get_event_loop()
sp_client = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv("SPOTIFYCLIENTID"), client_secret=os.getenv("SPOTIFYCLIENTSECRET")))


class MusicPlayerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.disconnect_task = None
        
    def cancel_disconnect_time(self):
        if self.disconnect_task and not self.disconnect_task.done():
            self.disconnect_task.cancel()
            self.disconnect_task = None    
            
async def setup(bot):
    print("incantation cog setup")
    await bot.add_cog(MusicPlayerCog(bot))