import discord
import discord.ext



class HelpEmbed(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.currentpage = 0
        
    @discord.ui.button(label='Page 1', style=discord.ButtonStyle.primary)
    async def page_1(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.currentpage != 1:
            self.currentpage = 1
            await interaction.response.edit_message(embed=discord.Embed(title="Help - Page 1", description="List of commands for Page 1"))
    
    @discord.ui.button(label='Page 2', style=discord.ButtonStyle.primary)
    async def page_2(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.currentpage != 2:
            self.currentpage = 2
            #figure out how to add more than one line to the interaction edit
            await interaction.response.edit_message(embed=discord.Embed(title="Help - Page 2", description="List of commands for Page 2"))