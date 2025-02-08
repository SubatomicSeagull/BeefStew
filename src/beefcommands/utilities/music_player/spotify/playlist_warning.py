import discord

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