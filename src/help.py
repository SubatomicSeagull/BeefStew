import discord
import discord.ext
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
        page1embed.add_field(name="", value="`/kick`: OOT MAH HOOSE", inline=False)
        page1embed.add_field(name="", value="`/ban`: KILL KILL KILL!!!", inline=False)
        await interaction.response.edit_message(embed=page1embed)
            
    @discord.ui.button(label="Utilities", style=discord.ButtonStyle.primary)
    async def page_2(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.currentpage = 2
        page2embed = discord.Embed(title="Help - Utilities", description="TOOLS!! i need my TOOLS!!!!!", color=discord.Color.lighter_grey())
        page2embed.add_field(name="Commands:",value="", inline=False)
        page2embed.add_field(name="", value="`/ccping`: pings ccserver, be sensible with this one", inline=False)
        page2embed.add_field(name="", value="`/ccinfo`: retrieve current info about CCServer", inline=False)
        page2embed.add_field(name="", value="`/logs`: sets the current channel as the logs channel", inline=False)
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
        await interaction.response.edit_message(embed=page4embed)
        
    @discord.ui.button(label="Visage", style=discord.ButtonStyle.primary)    
    async def page_5(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.currentpage = 5
        page5embed = discord.Embed(title="Help - Visage", description="alter the flesh, alter the mind...", color=discord.Color.lighter_grey())
        page5embed.add_field(name="Commands:",value="", inline=False)
        page5embed.add_field(name="", value="`/boil`: boils the user", inline=False)
        page5embed.add_field(name="", value="`/slander`: i cant belive they just said that...", inline=False)
        await interaction.response.edit_message(embed=page5embed)