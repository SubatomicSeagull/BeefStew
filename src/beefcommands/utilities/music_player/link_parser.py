import re
import discord
from beefcommands.utilities.music_player.youtube.yt_query_constructor import get_metadata_yt, yt_search_term
from beefcommands.utilities.music_player.spotify.spotify_link_parser import spotify_link_parser

async def link_validation(url: str):
    print("validating the link")
    youtube_pattern = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+')
    spotify_pattern = re.compile(r'(https?://)?(open\.)?spotify\.com/.+')
    search_pattern = re.compile(r'^(?!https?://).+')

    if youtube_pattern.match(url):
        return "youtube"
    elif spotify_pattern.match(url):
        return "spotify"
    elif search_pattern.match(url):
        return "search"
    else:
        return "invalid"

async def media_source(interaction: discord.Interaction, url: str):
    if type == 'youtube':
        print("youtube link, retrieving metadata")
        return await get_metadata_yt(interaction, url)
    elif type == 'spotify':
        print("spotify link, retrieving metadata")
        return await spotify_link_parser(interaction, url)
    elif type == 'search':
        print("search term, retrieving yt link")        
        return await yt_search_term(interaction, url)
    else:
        return "invalid"
        

