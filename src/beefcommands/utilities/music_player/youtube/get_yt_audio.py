import discord
from beefcommands.utilities.music_player.link_parser import media_source

async def get_audio_link(interaction: discord.Interaction, url: str):
    print(f"putting {url} throught the link parser...")
    metadata = await media_source(interaction, url)
    return metadata["url"]