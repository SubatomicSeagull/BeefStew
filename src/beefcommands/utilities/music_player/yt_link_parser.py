import re
import discord

async def link_validation(url: str):
    print("validating the link")
    youtube_pattern = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+')
    spotify_pattern = re.compile(r'(https?://)?(open\.)?spotify\.com/.+')
    search_pattern = re.compile(r'^(?!https?://).+')

    if youtube_pattern.match(url):
        return True, "youtube"
    elif spotify_pattern.match(url):
        return True, "spotify"
    elif search_pattern.match(url):
        return True, "search"
    else:
        return False, "invalid"

async def link_parser(interaction: discord.Interaction, url: str):
    (valid, type) = await link_validation(url)
    
    if type == 'youtube':
        print("youtube link, retrieving metadata")
        return await get_metadata_yt(interaction, url)
    elif type == 'spotify':
        print("spotify link, retrieving metadata")
        return await spotify_link_parser(interaction, url)
    elif type == 'search':
        print("search term, retrieving yt link")        
        return await yt_search(interaction, url)

async def get_audio_link(interaction: discord.Interaction, url: str):
    print(f"putting {url} throught the link parser...")
    metadata = await link_parser(interaction, url)
    return metadata["url"]