import discord
import discord.ext

#todo
# needs updating plz

async def help(bot, interaction: discord.Interaction):
    await interaction.response.defer()
    # dm restriction
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send("we are literally in DMs rn bro u cant do that here...")
        return
    
    # embed header
    view = HelpEmbed()
    page0embed = discord.Embed(title="Beefstew Help", description="You don't want to know what I can *really* do...", color=discord.Color.lighter_grey())
    page0embed.set_thumbnail(url=bot.user.avatar.url)
    page0embed.set_author(name="Help", icon_url=bot.user.avatar.url)
    #embed body
    page0embed.add_field(name="",value="⠀", inline=False)
    page0embed.add_field(name="Commands:",value="", inline=False)
    page0embed.add_field(name="",value="Click on the buttons below for a list of commands", inline=False)
    page0embed.add_field(name="",value="⠀", inline=False)
    page0embed.add_field(name="\nOther info:\n",value="", inline=False)
    page0embed.add_field(name="", value="Privacy Policy", inline=True)
    page0embed.add_field(name="", value="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Terms of Service", inline=True)
    # embed footer
    page0embed.add_field(name="", value="[cosycraft.uk/privacy](https://www.cosycraft.uk/privacy)⠀⠀⠀⠀⠀⠀⠀[cosycraft/tos](https://www.cosycraft.com/tos)", inline=False)
    await interaction.channel.send(embed=page0embed, view=view)

class HelpEmbed(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.currentpage = 0
        
    @discord.ui.button(label="Moderation", style=discord.ButtonStyle.primary)
    async def page_1(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.currentpage = 1
        page1embed = discord.Embed(title="Help - Moderation", description="judge judy, and exeggutor", color=discord.Color.lighter_grey())
        page1embed.add_field(name="Commands:",value="", inline=False)
        page1embed.add_field(name="", value="`/warn`: 🫵YOU", inline=False)
        page1embed.add_field(name="", value="`/mute`: SHHHHHHHHHH", inline=False)
        page1embed.add_field(name="", value="`/unmute`: HHHHHHHHHHS", inline=False)
        page1embed.add_field(name="", value="`/kick`: OOT MAH HOOSE", inline=False)
        page1embed.add_field(name="", value="`/ban`: KILL KILL KILL!!!", inline=False)
        await interaction.response.edit_message(embed=page1embed)
            
    @discord.ui.button(label="Utilities", style=discord.ButtonStyle.primary)
    async def page_2(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.currentpage = 2
        page2embed = discord.Embed(title="Help - Utilities", description="TOOLS!! i need my TOOLS!!!!!", color=discord.Color.lighter_grey())
        page2embed.add_field(name="Commands:",value="", inline=False)
        page2embed.add_field(name="", value="`/ccping`: pings ccserver, be sensible with this one", inline=False)
        #page2embed.add_field(name="", value="`/ccinfo`: retrieve current info about CCServer", inline=False)
        page2embed.add_field(name="", value="`/set_logs`: sets the current channel as the logs channel", inline=False)
        page2embed.add_field(name="", value="`/set_info`: sets the current channel as the info channel", inline=False)
        page2embed.add_field(name="", value="`/set_quotes`: sets the current channel as the quotes channel", inline=False)
        page2embed.add_field(name="", value="`/update`: whats new?", inline=False)
        page2embed.add_field(name="", value="`/test`: <- jamie delete this", inline=False)
        await interaction.response.edit_message(embed=page2embed)
            
    @discord.ui.button(label="Incantations", style=discord.ButtonStyle.primary)
    async def page_3(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.currentpage = 3
        page3embed = discord.Embed(title="Help - Incantations", description="nuns commence incating as the lighting strikes mine temples", color=discord.Color.lighter_grey())
        page3embed.add_field(name="Commands:",value="", inline=False)
        page3embed.add_field(name="", value="`/mock`: cast vicious mockery on someone", inline=False)
        await interaction.response.edit_message(embed=page3embed)
            
    @discord.ui.button(label="Invocations", style=discord.ButtonStyle.primary)    
    async def page_4(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.currentpage = 4
        page4embed = discord.Embed(title="Help - Invocations", description="let ye who is without sin cast the first stone", color=discord.Color.lighter_grey())
        page4embed.add_field(name="Commands:",value="", inline=False)
        page4embed.add_field(name="", value="`[@victim] they call you [nickname]`: invoke the rule...", inline=False)
        page4embed.add_field(name="", value="`[@victim] +2`: good joke <:beefsmile:1308701407007739974>", inline=False)
        page4embed.add_field(name="", value="`[@victim] -2`: bad joke <:beefhusk:1287094093989679124>", inline=False)
        page4embed.add_field(name="", value="`/leaderboard`: top 10 jokers", inline=False)
        page4embed.add_field(name="", value="`/loserboard`: bottom 10 jokers", inline=False)
        page4embed.add_field(name="", value="`/gamble`: spend a joke point to gamble it all...", inline=False)     
        page4embed.add_field(name="", value="`/score`: how funny r u?", inline=False)
        await interaction.response.edit_message(embed=page4embed)
        
    @discord.ui.button(label="Visage", style=discord.ButtonStyle.primary)    
    async def page_5(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.currentpage = 5
        page5embed = discord.Embed(title="Help - Visage", description="alter the flesh, alter the mind...", color=discord.Color.lighter_grey())
        page5embed.add_field(name="Commands:",value="", inline=False)
        page5embed.add_field(name="", value="`/boil`: boils the user", inline=False)
        page5embed.add_field(name="", value="`/slander`: i cant belive they just said that...", inline=False)
        page5embed.add_field(name="", value="`/drain`: yea we dropped them down there they got stucl ://", inline=False)
        page5embed.add_field(name="", value="`/bless`: bless you my child...", inline=False)
        page5embed.add_field(name="", value="`/jail`: go directly to jail!", inline=False)
        page5embed.add_field(name="", value="`/jfk`: MISTER PRESIDENT WATCH OUT", inline=False)

        await interaction.response.edit_message(embed=page5embed)
        
    @discord.ui.button(label="Music Player", style=discord.ButtonStyle.primary)    
    async def page_6(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.currentpage = 6
        page5embed = discord.Embed(title="Help - Music Player", description="DJ DJ DDDD DJ DJ        DJ", color=discord.Color.lighter_grey())
        page5embed.add_field(name="Commands:",value="", inline=False)
        page5embed.add_field(name="", value="The music player can take tracks from:\n Direct youtube links (e.g youtube.com/watch____)\nSpotify links (e.g open.spotify.com/track/______)\n Search Terms (e.g 'jellyish fields forever')", inline=False)
        page5embed.add_field(name="", value="`/play [link]`: adds the track to the front of the queue and starts playing", inline=False)
        page5embed.add_field(name="", value="`/queue [link]`: adds the track to the back of the queue", inline=False)
        page5embed.add_field(name="", value="`/pause`: pauses the current track", inline=False)
        page5embed.add_field(name="", value="`/resume`: resumes the current track", inline=False)
        page5embed.add_field(name="", value="`/skip`: skips the current track", inline=False)
        page5embed.add_field(name="", value="`/list`: lists all tracks in the queue", inline=False)
        page5embed.add_field(name="", value="`/shuffle`: shuffles the queue", inline=False)
        page5embed.add_field(name="", value="`/clear`: clears the queue", inline=False)
        page5embed.add_field(name="", value="`/loop`: loops the current track", inline=False)
        page5embed.add_field(name="", value="`/join`: joins the voice channel", inline=False)
        page5embed.add_field(name="", value="`/leave`: leaves the voice channel", inline=False)
        
        await interaction.response.edit_message(embed=page5embed)