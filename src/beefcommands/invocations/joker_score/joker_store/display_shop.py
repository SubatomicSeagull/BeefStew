import discord

class ShopView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(timeout = 60)
        self.chosen_item = None
        self.message = None
        self.interaction = interaction
    
    async def on_timeout(self):
        await self.message.delete()
        await display_shop_closed(self.interaction, "you took too long!!!!")
            
    @discord.ui.button(label = "item1", style = discord.ButtonStyle.green)
    async def item1(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.chosen_item = 1
        await interaction.response.defer()
        self.stop()

    @discord.ui.button(label = "item2", style = discord.ButtonStyle.primary)
    async def item2(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.chosen_item = 2
        await interaction.response.defer()
        self.stop()
    
    @discord.ui.button(label = "item3", style = discord.ButtonStyle.grey)
    async def item3(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.chosen_item = 3
        await interaction.response.defer()
        self.stop()
        
    @discord.ui.button(label = "item4", style = discord.ButtonStyle.red)
    async def item4(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.chosen_item = 4
        await interaction.response.defer()
        self.stop()
    
    @discord.ui.button(label = "item5", style = discord.ButtonStyle.danger)
    async def item5(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.chosen_item = 5
        await interaction.response.defer()
        self.stop()

async def display_shop_open(interaction: discord.Interaction):
    await interaction.response.defer()
    await shop_embed_open(interaction)

async def shop_embed_open(interaction: discord.Interaction):
    shopembed = discord.Embed(title="beefstore", description="welcome", color=discord.Color.blue())
    shopembed.set_image(url = "https://tenor.com/view/hi-gif-1459774218829111523")
    view = ShopView(interaction)
    
    msg = await interaction.followup.send(embed=shopembed, view=view)
    view.message = msg
    await view.wait()
    
    if view.chosen_item is None:
        return
    
    await msg.edit(content=f"bought item {view.chosen_item}...", embed=None, view=None)
    
    await display_shop_closed(interaction, "thank you for your patronage!")
    
async def display_shop_closed(interaction: discord.Interaction, message: str):
    await shop_embed_closed(interaction, message)

async def shop_embed_closed(interaction: discord.Interaction, message: str):
    shopembed = discord.Embed(title="beefstore", description="no", color=discord.Color.dark_orange())
    shopembed.set_image(url="https://tenor.com/view/bye-sad-waving-face-gif-5637274149426828892")
    await interaction.channel.send(content=message, embed=shopembed)
