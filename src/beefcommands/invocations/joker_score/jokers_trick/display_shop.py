import discord

class ShopView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(timeout = 60)
        self.chosen_item = None
        self.message = None
        self.interaction = interaction
    
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.interaction.user.id:
            await interaction.response.send_message("Hey! get in line buddy >:( if you wanna buy something use `/shop` yourself!", ephemeral=True)
            return False
        return True
    
    async def on_timeout(self):
        await self.interaction.response.edit_message(content="Took too long buddy! NEXT!!!", embed=None, view=None)
        self.stop()

                    
    @discord.ui.button(label = "-2 Shield", style = discord.ButtonStyle.green)
    async def item1(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.chosen_item = 1
        await interaction.response.edit_message(content="Thank you for your purchase!", embed=None, view=None)
        self.stop()

    @discord.ui.button(label = "Uno Reverse", style = discord.ButtonStyle.primary)
    async def item2(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.chosen_item = 2
        await interaction.response.edit_message(content="Thank you for your purchase!", embed=None, view=None)
        self.stop()
    
    @discord.ui.button(label = "Multiplier", style = discord.ButtonStyle.grey)
    async def item3(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.chosen_item = 3
        await interaction.response.edit_message(content="Thank you for your purchase!", embed=None, view=None)
        self.stop()
        
    @discord.ui.button(label = "Charity", style = discord.ButtonStyle.red)
    async def item4(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.chosen_item = 4
        await interaction.response.edit_message(content="Thank you for your purchase!", embed=None, view=None)
        self.stop()
    
    @discord.ui.button(label = "Revolution", style = discord.ButtonStyle.danger)
    async def item5(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.chosen_item = 5
        await interaction.response.edit_message(content="Thank you for your purchase!", embed=None, view=None)
        self.stop()

async def display_shop_open(interaction: discord.Interaction):
    await shop_embed_open(interaction)

async def shop_embed_open(interaction: discord.Interaction):
    shopembed = discord.Embed(title="beefstore", description="welcome", color=discord.Color.blue())
    shopembed.set_image(url = "https://tenor.com/view/hi-gif-1459774218829111523")
    view = ShopView(interaction)
    
    msg = await interaction.response.send_message(embed=shopembed, view=view, ephemeral=True)
    view.message = msg
    await view.wait()
    if view.chosen_item is None:
        return
    
    print(f"bought item {view.chosen_item}")
