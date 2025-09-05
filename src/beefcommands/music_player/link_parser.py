
# what kind of link is it?
import asyncio
import html
import math
import re
import discord
import requests
import urllib
from main import bot, sp_client #<- badddd


async def parse(tx_channel, url, type):
    return_links = []
    if type == 'youtube':
        title = await get_youtube_title(url)
        return_links.append([(url, title)])
    elif type == 'spotify':
        sp_song = await spotify_link_parser(tx_channel, url)
        return_links.append(sp_song)
    elif type == 'search':
        search_song = await get_youtube_link(url)
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

async def get_youtube_title(url):
    # retrieve the thread executor loop
    loop = asyncio.get_running_loop()

    # retrieve the youtube link title in a different thread
    return await loop.run_in_executor(bot.executor, sync_get_youtube_title, url)

def sync_get_youtube_title(url):
    if url is not None or "":
        # retrieve the html header data from the youtube link as text
        response  = requests.get(url)
        htmlresponse = response.text

        # regex pattern to retrieve only the title
        title_match = re.search(r'<title>(.*?) - YouTube</title>', htmlresponse)
        if title_match:
            # take out the "- Youtube"
            title = title_match.group(1).strip()

            if title == "":
                return "Empty :("

            # return the UTF-8 title from the html data
            return html.unescape(title)
    return "Unknown"

async def get_youtube_link(search_term):
    # retrieve the thread executor loop
    loop = asyncio.get_running_loop()

    # generate the youtube link in a different thread
    return await loop.run_in_executor(bot.executor, sync_get_youtube_link, search_term)

def sync_get_youtube_link(search_term):
    try:
        # replace spaces in the query with +
        phrase = urllib.parse.quote(search_term.replace(" ", "+"), safe="+")

        # construct the youtube link
        search_link = f"https://www.youtube.com/results?search_query={phrase}"

        # retrieve the videos given by the link
        response = urllib.request.urlopen(search_link)
        search_results = re.findall(r'watch\?v=(\S{11})', response.read().decode())

        # return the first result
        return f"https://www.youtube.com/watch?v={search_results[0]}"

    except Exception as e:
        return None

async def spotify_link_parser(tx_channel, url):
    # retrieve the thread executor pool
    loop = asyncio.get_running_loop()

    # https://open.spotify.com/track/...........
    # retrieve the metadata of the given spotify track on a different thread
    if "track" in url:
        track = await loop.run_in_executor(bot.executor, sp_client.track, url)
        return [await process_spotify_track(track)]

    # https://open.spotify.com/album/...........
    # retrieve the metadata for an album on a different thread and return it to an array
    if "album" in url:
        album_tracks = await loop.run_in_executor(bot.executor, sp_client.album_tracks, url)
        urls = []
        fetch_album_tracks = await asyncio.gather(*[process_spotify_track(track)for track in album_tracks["items"]])
        for result in fetch_album_tracks:
            if result is not None:
                urls.append(result)
        return urls

    #https://open.spotify.com/playlist/...........
    # retrieve the metadata for a playlist on a different thread
    if "playlist" in url:
        playlist = await loop.run_in_executor(bot.executor, sp_client.playlist, url)
        playlist_name = playlist['name']
        playlist_art = playlist['images'][0]['url'] if playlist['images'] else None
        total = playlist['tracks']['total']

        # call the playlist warning
        warning_response = await playlistwarning(tx_channel, playlist_name, playlist_art, total)
        if warning_response is None:
            return []

        # process each track of each page of the playlist in a the thread pool and add it to an array
        urls = []

        # retrieve the metadata for the playlist track
        song_list = await loop.run_in_executor(bot.executor, sp_client.playlist_tracks, url)

        # calculate the number of pages
        total = song_list["total"]
        pages = math.ceil(total / 100)

        # if the user wants to add all the songs, process each track for each page
        if warning_response == True:
            for i in range(pages):
                print(i)
                page = sp_client.playlist_tracks(url, offset = i * 100)
                fetch_page = await asyncio.gather(*[process_spotify_track(item["track"]) for item in page["items"]])
                for result in fetch_page:
                    if result is not None:
                        urls.append(result)
        return urls

    # cant process and artist list
    if "artist" in url:
        return None


async def process_spotify_track(track):
    # retrieve the name and artist
    try:
        song_name = track["name"]
        artist = track['artists'][0]['name']
    except Exception as e:
        return None

    # define a search query "ARTIST - SONG NAME"
    search_term = f"{artist} - {song_name}"
    try:
        # send the query to the youtube link parser
        yt_link = await get_youtube_link(search_term)
        title = await get_youtube_title(yt_link)
        return (yt_link, title)

    # sometimes it cant parse the title
    except Exception as e:
        return None


class PlaylistWarningEmbed(discord.ui.View):
    def __init__(self, tx_channel):
        super().__init__(timeout=30)
        self.tx_channel = tx_channel
        self.response = None
        self.message = None

    @discord.ui.button(label="all of em babey!!", style=discord.ButtonStyle.green)
    async def add_all_tracks(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.response = True
        await interaction.message.delete()
        self.stop()

    @discord.ui.button(label="umm actaully nvm ://", style=discord.ButtonStyle.danger)
    async def dont_add_tracks(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.response = None
        await interaction.message.delete()
        self.stop()

    async def on_timeout(self):
        if self.message:
            try:
                await self.message.delete()
            except discord.NotFound:
                pass
        self.stop()

async def playlistwarning(tx_channel, playlist_name, playlist_art, count):
    warning_embed = discord.Embed(title=playlist_name, description="hold on there buddy...", color=discord.Color.green())

    # sets the thumbnail to be the playlist art
    warning_embed.set_thumbnail(url=playlist_art)
    warning_embed.add_field(name="", value=f"**{playlist_name}** has **{count}** songs, do you want to add them all?")

    view = PlaylistWarningEmbed(tx_channel)

    message = await tx_channel.send(embed=warning_embed, view=view)
    view.message = message

    # wait for a user to click a button, else, timeout
    await view.wait()
    return view.response