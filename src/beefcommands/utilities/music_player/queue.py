import discord
import random

queue = []

async def queue_stack(self, interaction: discord.Interaction, tracks: list):
    await interaction.response.send_message("not implemented yet sorry :(")
    queue.insert(0, tracks[0])
    
async def queue_push(self, interaction: discord.Interaction, tracks: list):
    await interaction.response.send_message("not implemented yet sorry :(")
    for track in tracks:
        queue.append(track)
    
async def queue_pop(self, interaction: discord.Interaction):
    await interaction.response.send_message("not implemented yet sorry :(")
    queue.pop(0)
    
async def clear(self, interaction: discord.Interaction):
    await interaction.response.send_message("not implemented yet sorry :(")
    queue.clear()
    
async def shuffle(self, interaction: discord.Interaction):
    await interaction.response.send_message("not implemented yet sorry :(")
    random.shuffle
    
async def queue_list(self, interaction: discord.Interaction):
    for track in queue:
        print(track)
    #generate an embed listing the first 10 songs in the queue,
    # is there a way to dynamically add pages?
    
async def queue_embed(self, interaction: discord.Interaction):
    pass
#generate a queue embed
# "xyz added abc to the back/front queue"