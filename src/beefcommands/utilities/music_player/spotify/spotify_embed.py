import discord

async def playlist_warning(interaction: discord.Interaction, playlist_art: str, count: int, name: str):  
    view = PlaylistWarningEmbed()
    embed = discord.Embed(title="Spotify Playlist", description="hold on there buddy...", color=discord.Color.green())
    embed.set_thumbnail(url=playlist_art)
    embed.add_field(name=f"{name} has {count} songs.", value= "u wanna add all these?")
    await interaction.response.send_message(embed=embed, view=view)
    
    await view.wait()
    response = view.response

    return response
class PlaylistWarningEmbed(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.response = None
        
    @discord.ui.button(label="all of em babey!!", style=discord.ButtonStyle.primary)
    async def add_all_tracks(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.response = True
        self.stop()
        await interaction.response.edit_message(content="added all the tracks", embed=None, view=None)
    
    @discord.ui.button(label= "just the one please", style=discord.ButtonStyle.primary)
    async def add_top_track(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.response = False
        self.stop()
        await interaction.response.edit_message(content="added one track", embed=None, view=None)