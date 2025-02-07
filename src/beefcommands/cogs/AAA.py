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
import time
import html
import math
import random



#todo
# can we get rid of these globals?
# splice everything up neatly

g_queue = []
g_current_track = []
g_loop = False
executor = ThreadPoolExecutor(max_workers=4)
asyncloop = asyncio.get_event_loop()
sp_client = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv("SPOTIFYCLIENTID"), client_secret=os.getenv("SPOTIFYCLIENTSECRET")))

class testCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.paused_position = 0
        self.paused_source = None
        self.start_time = None
        
        
    def get_queue(self):
        return g_queue
    
    def get_current_track(self, track):
        return g_current_track
    
    def get_current_track_link(self):
        return g_current_track[0][0]
    
    def get_current_track_title(self):
        return g_current_track[0][1]
    
    def set_current_track(self, track):
        g_current_track.clear()
        g_current_track.append(track)
        
    def get_loop_flag(self):
        return g_loop
    
    def set_loop_flag(self, value):
        loop = value
        
    @commands.command(name="skip", description="next pleaes")
    async def skip(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await self.play_next(ctx)
    
    # add alias "/queue", "/q"  
    @commands.command(name="qadd", description="list the queue")  
    async def qadd(self, ctx, *args):
        url = " ".join(args)
        await handle_queue(ctx, url)
        
    @commands.command(name="qlist", description="list the queue")
    async def qlist(self, ctx):
        queue = self.get_queue()
        if not queue:
            await ctx.send("the queue is empty")
            return
        
        content = "**Queue:**\n"
        for i in range(len(queue)):
            print(queue[i])
            if i < 10:
                content += f"{i}. {queue[i][1]}\n"
            else:
                content += f"... and {len(queue) - 10} more tracks."
                break
            
        await ctx.send(content)
        
    @commands.command(name="qinsert", description="insert the song at the front of the queue")
    async def qinsert(self, ctx, *args):
        url = " ".join(args)
        await handle_queue(ctx, url, insert=True)

    @commands.command(name="qclear", description="clears the queue")
    async def qclear(self, ctx):
        self.get_queue().clear()
        await ctx.send(f"{ctx.author.name} cleared the queue")

    @commands.command(name="qpop", description="take the first item off the queue")
    async def qpop(self, ctx):
        queue = self.get_queue()
        if queue:
            queue.pop(0)

    @commands.command(name="shuffle", description="lol XD random")
    async def shuffle(self, ctx):
        queue = self.get_queue()
        random.shuffle(queue)
        await ctx.send(f"{ctx.author.name} shuffled the queue")
    

    @commands.command(name="loop", description="loops the current song")
    async def loop(self, ctx):
        if self.get_loop_flag() == False:
            self.set_loop_flag(True)
            await ctx.send(f"toggled loop **ON**")
        else:
            self.set_loop_flag(False)
            await ctx.send(f"toggled loop **OFF**")

    # add alias "/p"
    @commands.command(name="play", description="play the funky music white boy")
    async def play(self, ctx, *args):
        if not ctx.author.voice:
            await ctx.reply("ur not in a vc")
            return
        
        url = " ".join(args)
        if url:
            await handle_queue(ctx, url, insert=True)
            print("establishing voice connection")
            await self.establish_voice_connection(ctx)
            print("playing next")
        
            if not (ctx.voice_client and ctx.voice_client.is_playing()):
                await self.play_next(ctx)
    
    
    @commands.command(name="qpause", description="Pause the current track")
    async def qpause(self, ctx):
        print("PAUSING")
        if ctx.voice_client and ctx.voice_client.is_playing():
            if self.start_time:
                self.paused_position = (ctx.message.created_at - self.start_time).total_seconds()
            self.paused_source = ctx.voice_client.source
            ctx.voice_client.pause()
            print("PAUSED SUCCESSFULLY")

    @commands.command(name="qresume", description="Resume the paused track")
    async def qresume(self, ctx):
        print("RESUMING")
        if ctx.voice_client and ctx.voice_client.is_paused():
            # Resume from the stored position
            exepath = os.getenv("FFMPEGEXE")
            source = discord.FFmpegPCMAudio(
                source=self.paused_source.original,
                executable=exepath,
                before_options=f"-ss {self.paused_position}"
            )
            
            ctx.voice_client.play(source, after=lambda e: self.bot.loop.create_task(self.handle_after_playing(ctx, e)))
            print("RESUMED SUCCESSFULLY")
            self.start_time = ctx.message.created_at - time.timedelta(seconds=self.paused_position)
    
    
    
    async def establish_voice_connection(self, ctx):
        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()
        elif ctx.voice_client.channel != ctx.author.voice.channel:
            await ctx.voice_client.move_to(ctx.author.voice.channel)
            
    async def play_next(self, ctx):
        queue = self.get_queue()
        
        if not queue and self.get_loop_flag() == False:
            await ctx.send("YAAAWNNN thers no more songs in the queue IM BORED!!! cya")
            await ctx.voice_client.disconnect()
            return
        
        if self.get_loop_flag == True and self.get_current_track():
            current_track = self.get_current_track()
        elif queue:
            current_track = queue.pop(0)
            self.set_current_track(current_track)
        else:
            return
        
        await self.play_track(ctx, current_track[0], current_track[1])
        
    async def play_track(self, ctx, url, title):
        exepath = os.getenv("FFMPEGEXE")
        
        ydl_ops = {
            "format": "bestaudio/best",
            "noplaylist": True,
            "quiet": True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_ops) as ydl:
                metadata = ydl.extract_info(url, download=False)
                audio_url = metadata["url"]   
        except Exception as e:
            await ctx.send(f"couldnt play {title} ({e})")
            return
        
        source = discord.FFmpegPCMAudio(source=audio_url, executable=exepath)
        
        def after_playing(error):
            if error:
                print(f"An error occurred: {error}")
                return
            coro = self.handle_after_playing(ctx, error)
            future = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
            try:
                future.result()
            except:
                pass
            
        ctx.voice_client.play(source, after=after_playing)
        await ctx.send(f"now playing: **{title}**")
            
            
    async def handle_after_playing(self, ctx, error):
        if self.get_loop_flag:
            current_track = self.get_current_track()
            if current_track:
                await self.play_track(ctx, current_track[0], current_track[1])
        else:
            await self.play_next(ctx)
    
    @commands.command(name="pause", description="STOP!!!")
    async def pause(self, ctx):
        #find some way to pause the track at the current time and resume it when sent /play again?
        pass
    
    # add inline command "(@)beefstew get in here", "(@)beefstew come here", 
    @commands.command(name="join", description="get in here!!")
    async def join_vc(self, ctx):
        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()
        elif ctx.voice_client.channel != ctx.author.voice.channel:
            await ctx.voice_client.move_to(ctx.author.voice.channel)
    
    # add alias "/fuckoff"
    @commands.command(name="leave", description="fukoff")
    async def leave(self, ctx):
        if ctx.voice_client:
            self.get_queue().clear()
            g_current_track.clear()
            await ctx.voice_client.disconnect()
        
async def setup(bot):
    print("incantation cog setup")
    await bot.add_cog(testCog(bot))





    
#=======================================================END OF COG============================================================
#=======================================================END OF COG============================================================
#=======================================================BEGINNING OF FUNCTIONS================================================




async def handle_queue(ctx, url, insert=False):
    media_type = validate_input(url)
    if media_type == "invalid":
        await ctx.send("invalid link")
        return
    
    ytlinks = await link_parser(ctx, url, media_type)
    if not ytlinks:
        await ctx.send("failed to get youtube link")
        return
    
    queue = testCog.get_queue(testCog)
    added = 0
    print(ytlinks)
    for playlist in ytlinks:
        for track in playlist:
            if insert:
                print(f"inserting {track}")
                queue.insert(0, track)
            else:
                print(f"appending {track}")
                queue.append(track)
            added += 1
        
    if added == 1:
        await ctx.send(f"{ctx.author.name} added 1 track to the queue")
    else:
        await ctx.send(f"{ctx.author.name} added {added} tracks to the queue")
        
async def get_youtube_title(url):
    return await asyncloop.run_in_executor(executor, sync_get_youtube_title, url)
    
def sync_get_youtube_title(url):
    if url is not None or "":
        response  = requests.get(url)
        htmlresponse = response.text
        title_match = re.search(r'<title>(.*?) - YouTube</title>', htmlresponse)
        if title_match:
            title = title_match.group(1).strip()
            if title == "":
                print("TITLE IS EMPTY!!!!!!!")
                return "Empty :("
            print(f"returning title {html.unescape(title)}")
            return html.unescape(title)
    
    return "Unknown"

def validate_input(url):
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
    
def get_metadata_youtube(ctx, url):
    print("getting metadata for youtube")
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict
    
async def get_youtube_link(ctx, search_term):
    return await asyncloop.run_in_executor(executor, sync_get_youtube_link, search_term)
    
def sync_get_youtube_link(search_term):
    print(f"getting youtube link for {search_term}")
    try:
        phrase = urllib.parse.quote(search_term.replace(" ", "+"), safe="+")
        search_link = f"https://www.youtube.com/results?search_query={phrase}"
        response = urllib.request.urlopen(search_link)
        search_results = re.findall(r'watch\?v=(\S{11})', response.read().decode())
        return f"https://www.youtube.com/watch?v={search_results[0]}"
    except Exception as e:
        return None
    
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

async def spotify_link_parser(ctx, url):
    if "track" in url:
        print("getting metadata for spotify track")

        track = await asyncloop.run_in_executor(executor, sp_client.track, url)
        return [await process_spotify_track(ctx, track)]
    
    if "album" in url:
        album_tracks = await asyncloop.run_in_executor(executor, sp_client.album_tracks, url)
        urls = []
        print("getting metadata for spotify album")
        fetch_album_tracks = await asyncio.gather(*[process_spotify_track(ctx, track)for track in album_tracks["items"]])
        for result in fetch_album_tracks:
            if result is not None:
                urls.append(result)
        return urls
        
    if "playlist" in url:
        playlist = await asyncloop.run_in_executor(executor, sp_client.playlist, url)
        playlist_name = playlist['name']
        playlist_art = playlist['images'][0]['url'] if playlist['images'] else None
        total = playlist['tracks']['total']
        warning_response = await playlistwarning(ctx, playlist_name, playlist_art, total)
        if warning_response is None:
            return []
        
        urls = []
        print("getting metadata for spotify playlist")
        song_list = await asyncloop.run_in_executor(executor, sp_client.playlist_tracks, url)
        total = song_list["total"]
        pages = math.ceil(total / 100)
        
        if warning_response == True:    
            for i in range(pages):
                print(f"fetching page {i}")
                page = sp_client.playlist_tracks(url, offset = i * 100)
                fetch_page = await asyncio.gather(*[process_spotify_track(ctx, item["track"]) for item in page["items"]])
                for result in fetch_page:
                    if result is not None:
                        urls.append(result)
        return urls

    if "artist" in url:
        print("artist link... whajt r u doing")
        return None
    
    
async def process_spotify_track(ctx, track):
    song_name = track["name"]
    artist = track['artists'][0]['name']
    search_term = f"{artist} - {song_name}"
    try:
        yt_link = await get_youtube_link(ctx, search_term)
        title = await get_youtube_title(yt_link)
        return (yt_link, title)
    except Exception as e:
        print(f"\n \n ==========================failed to process track {song_name}, skipping. ({e})==================== \n \n )")
        return None 

class PlaylistWarningEmbed(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.response = None
        self.message = None
        
    @discord.ui.button(label="all of em babey!!", style=discord.ButtonStyle.primary)
    async def add_all_tracks(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.response = True
        await interaction.message.delete()
        self.stop()
    
    @discord.ui.button(label="just the one please", style=discord.ButtonStyle.primary)
    async def add_top_track(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.response = False
        await interaction.message.delete()
        self.stop()
        
    @discord.ui.button(label="umm actaully nvm ://", style=discord.ButtonStyle.primary)
    async def add_top_track(self, interaction: discord.Interaction, button: discord.ui.Button):
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
        
async def playlistwarning(ctx, playlist_name, playlist_art, count):
    warning_embed = discord.Embed(title=playlist_name, description="hold on there buddy...", color=discord.Color.green())
    warning_embed.set_thumbnail(url=playlist_art)
    warning_embed.add_field(name="", value=f"**{playlist_name}** has **{count}** songs, do you want to add them all?")
    
    view = PlaylistWarningEmbed(ctx)
    message = await ctx.send(embed=warning_embed, view=view)
    view.message = message
    
    await view.wait()
    return view.response