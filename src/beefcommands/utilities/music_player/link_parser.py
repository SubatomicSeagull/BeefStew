import re
import yt_dlp
import urllib.request

#take in a hyperlink or search term
#using regex, find out which website it is for, or if its even a link at all
#supported sites: youtube, spotify, bandcamp, soundcloud
# find the metadata in non youtube links, then search and return the link for the first search result.

# for spotify playlists, ask user if they want to queue all X songs or just the first one.
# if yes, return list of sanitiesed yt links, no = just the first one 

#non hyperlinks can skip straight to the youtbe search

#youtube links can skip the search process entirely


def link_validation(url: str):
    print("validating the link")
    youtube_pattern = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+')
    spotify_pattern = re.compile(r'(https?://)?(open\.)?spotify\.com/.+')
    bandcamp_pattern = re.compile(r'(https?://)?([a-z0-9]+\.bandcamp\.com)/.+')
    soundcloud_pattern = re.compile(r'(https?://)?(www\.)?soundcloud\.com/.+')
    search_pattern = re.compile(r'^(?!https?://).+')

    if youtube_pattern.match(url):
        return True, "youtube"
    elif spotify_pattern.match(url):
        return True, "spotify"
    elif bandcamp_pattern.match(url):
        return True, "bandcamp"
    elif soundcloud_pattern.match(url):
        return True, "soundcloud"
    elif search_pattern.match(url):
        return True, "search"
    else:
        return False, "invalid"

def link_parser(url: str):
    (valid, type) = link_validation(url)
    
    if type == 'youtube':
        print("youtube link, retrieving metadata")
        return get_metadata_yt(url)
    elif type == 'spotify':
        print("spotify link, retrieving metadata")
        return get_metadata_spotify(url)
    elif type == 'bandcamp':
        print("bandcamp link, retrieving metadata")
        return get_metadata_bandcamp(url)
    elif type == 'soundcloud':
        print("soundcloud link, retrieving metadata")    
        return get_metadata_soundcloud(url)
    elif type == 'search':
        print("search term, retrieving yt link")        
        return yt_search(url)


def get_metadata_yt(url: str):
    print("getting yt metadata")
    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict

def get_metadata_spotify(url: str):
    
    
    
    pass

def validate_spotify_link(url: str):
    if re.search(r"^(https?://)?open\.spotify\.com/(playlist|track)/.+$", url):
    return sp_url


def get_metadata_bandcamp(url: str):
    pass

def get_metadata_soundcloud(url: str):
    pass

def yt_search(search_term: str):
    phrase = search_term.replace(" ", "+")
    search_link = "https://www.youtube.com/results?search_query=" + phrase
    response = urllib.request.urlopen(search_link)
    
    search_results = re.findall(r'watch\?v=(\S{11})', response.read().decode())
    first_result = search_results[0]
    url = "https://www.youtube.com/watch?v=" + first_result
    return get_metadata_yt(url)

def get_audio_link(url: str):
    metadata = link_parser(url)
    return metadata["url"]
    
