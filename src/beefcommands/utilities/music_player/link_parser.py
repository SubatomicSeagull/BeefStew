import re
from beefcommands.utilities.music_player.youtube.youtube_handler import get_youtube_title, get_youtube_link
from beefcommands.utilities.music_player.spotify.spotify_handler import spotify_link_parser

# what kind of link is it?
async def link_parser(ctx, url, type):
    return_links = []
    if type == 'youtube':
        title = await get_youtube_title(url)
        return_links.append([(url, title)])
    elif type == 'spotify':
        sp_song = await spotify_link_parser(ctx, url)
        return_links.append(sp_song)
    elif type == 'search':
        search_song = await get_youtube_link(ctx, url)
        title = await get_youtube_title(search_song)
        return_links.append([(search_song, title)])
    return return_links

# is it a valid link, if so, what type?
def validate_input(url):
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