import discord

class PlaylistWarningEmbed(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=30)
        self.ctx = ctx
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
        
async def playlistwarning(ctx, playlist_name, playlist_art, count):
    warning_embed = discord.Embed(title=playlist_name, description="hold on there buddy...", color=discord.Color.green())
    # sets the thumbnail to be the playlist art
    warning_embed.set_thumbnail(url=playlist_art)
    warning_embed.add_field(name="", value=f"**{playlist_name}** has **{count}** songs, do you want to add them all?")
    
    view = PlaylistWarningEmbed(ctx)
    
    message = await ctx.send(embed=warning_embed, view=view)
    view.message = message
    # wait for a user to click a button, else, timeout
    await view.wait()
    return view.response